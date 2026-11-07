import tempfile
import unittest
import io
import json
from unittest.mock import patch
from pathlib import Path
from app import CHECKS, Demo, Ollama, connect, learned_advice, run, validate_verdict, render_lesson


class PipelineTests(unittest.TestCase):
    def test_structured_example_preserves_source_and_cites_answer(self):
        data = {key: 'Teaching text' for key in ('title', 'familiar_problem', 'definition', 'why',
                'preparation', 'steps', 'not_retraining', 'recap')}
        data.update({'glossary': [{'term': 'Model', 'meaning': 'A computer program.'}],
                     'example': {'source_note': 'Saturday closing time is 1 pm.',
                                 'question': 'When does it close on Saturday?', 'answer': '1 pm.',
                                 'missing_question': 'When does it open on holidays?',
                                 'missing_answer': 'The note does not say.'},
                     'risks': ['Missing evidence', 'Outdated evidence'],
                     'exercise': {'question': 'Practice', 'answer': 'Answer'},
                     'quiz': [{'question': 'Check', 'answer': 'Answer'}]})
        lesson = render_lesson(data)
        self.assertIn('**Retrieved text [Note A]:** Saturday closing time is 1 pm.', lesson)
        self.assertIn('**Answer:** 1 pm. [Note A]', lesson)
        self.assertIn('**Response when evidence is missing:** The note does not say.', lesson)

    def test_invalid_live_evidence_is_repaired_once_and_logged(self):
        class Repairable(Ollama):
            def __init__(self):
                super().__init__('test-generator', 'test-judge', 'unused')
            def generate(self, payload):
                return Demo().generate({'previous_failures': [True]})
            def evaluate(self, lesson, sources, repair=None):
                verdict = Demo().evaluate(lesson, sources)
                if repair is None:
                    verdict['checks']['coverage']['evidence'] = 'fabricated evidence'
                return verdict
        report, shipped = self.execute(Repairable())
        self.assertTrue(shipped)
        attempt = report['attempts'][0]
        self.assertEqual(len(attempt['raw_evaluations']), 2)
        self.assertEqual(attempt['evaluation_repair_reason'], 'Invalid evidence for coverage')

    def test_invalid_live_evidence_after_repair_never_ships(self):
        class Unrepairable(Ollama):
            def __init__(self):
                super().__init__('test-generator', 'test-judge', 'unused')
            def generate(self, payload):
                return Demo().generate({'previous_failures': [True]})
            def evaluate(self, lesson, sources, repair=None):
                verdict = Demo().evaluate(lesson, sources)
                verdict['checks']['coverage']['evidence'] = 'fabricated evidence'
                return verdict
        report, shipped = self.execute(Unrepairable())
        self.assertFalse(shipped)
        self.assertEqual(report['status'], 'error')
        self.assertEqual(len(report['attempts'][0]['raw_evaluations']), 2)

    def test_live_adapter_requires_all_judge_checkpoints(self):
        response = io.BytesIO(json.dumps({'message': {'content': '{}'}}).encode())
        with patch('app.urllib.request.urlopen', return_value=response) as mocked:
            Ollama('generator', 'judge', 'http://localhost:11434').evaluate('lesson', {})
        request = mocked.call_args.args[0]
        body = json.loads(request.data)
        self.assertEqual(body['model'], 'judge')
        checks = body['format']['properties']['checks']
        self.assertEqual(set(checks['required']), set(CHECKS))
        self.assertFalse(checks['additionalProperties'])
        for checkpoint in checks['properties'].values():
            self.assertEqual(checkpoint['properties']['pass']['type'], 'boolean')

    def test_live_evidence_line_ids_resolve_to_original_text(self):
        verdict = {'checks': {key: {'pass': True, 'reason': 'test', 'evidence': '2'} for key in CHECKS}}
        response = io.BytesIO(json.dumps({'message': {'content': json.dumps(verdict)}}).encode())
        with patch('app.urllib.request.urlopen', return_value=response) as mocked:
            result = Ollama('generator', 'judge', 'http://localhost:11434').evaluate('Heading\nExact evidence.', {})
        self.assertEqual(result['checks']['accuracy']['evidence'], 'Exact evidence.')
        self.assertEqual(result['checks']['accuracy']['evidence_line'], '2')
        validate_verdict(result, 'Heading\nExact evidence.')
        schema = json.loads(mocked.call_args.args[0].data)['format']
        self.assertEqual(schema['properties']['checks']['properties']['coverage']['properties']['evidence']['enum'],
                         ['MISSING', '1', '2'])

    def execute(self, backend, retries=2):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            report, target = run(backend, root / 'out', root / 'memory.sqlite', 'demo', retries)
            return report, (target / 'lesson.md').exists()

    def test_deliberate_error_is_repaired(self):
        report, shipped = self.execute(Demo())
        self.assertTrue(shipped)
        self.assertEqual(report['status'], 'passed')
        self.assertEqual(len(report['attempts']), 2)
        self.assertEqual(report['attempts'][0]['failures'][0]['checkpoint'], 'accuracy')
        self.assertNotIn('guarantees every answer', report['attempts'][1]['lesson'])

    def test_retry_exhaustion_does_not_ship(self):
        class AlwaysBad(Demo):
            def generate(self, payload):
                return super().generate({'previous_failures': []})
        report, shipped = self.execute(AlwaysBad())
        self.assertFalse(shipped)
        self.assertEqual(report['status'], 'rejected')
        self.assertEqual(len(report['attempts']), 3)

    def test_malformed_judge_blocks_release(self):
        class BadJudge(Demo):
            def evaluate(self, lesson, sources):
                return {'checks': {}}
        report, shipped = self.execute(BadJudge())
        self.assertEqual(report['status'], 'error')
        self.assertFalse(shipped)

    def test_boolean_strings_and_fabricated_evidence_rejected(self):
        lesson = '# Introduction to RAG'
        raw = Demo().evaluate(lesson, {})
        raw['checks']['accuracy']['pass'] = 'true'
        with self.assertRaises(ValueError):
            validate_verdict(raw, lesson)
        raw['checks']['accuracy']['pass'] = True
        raw['checks']['accuracy']['evidence'] = 'not in lesson'
        with self.assertRaises(ValueError):
            validate_verdict(raw, lesson)

    def test_persistent_memory_threshold_and_mode_isolation(self):
        with tempfile.TemporaryDirectory() as temp:
            dbpath = Path(temp) / 'memory.sqlite'
            for _ in range(2):
                run(Demo(), Path(temp) / 'out', dbpath, 'demo')
            db = connect(dbpath)
            self.assertIn('accuracy', learned_advice(db, 'Introduction to RAG', 'demo'))
            self.assertEqual(learned_advice(db, 'Introduction to RAG', 'live'), {})
            self.assertEqual(learned_advice(db, 'Other topic', 'demo'), {})
            db.close()

    def test_zero_retries(self):
        report, shipped = self.execute(Demo(), 0)
        self.assertEqual(len(report['attempts']), 1)
        self.assertFalse(shipped)

    def test_transport_failure_blocks_release(self):
        class Broken(Demo):
            def generate(self, payload):
                raise OSError('Network unavailable')
        report, shipped = self.execute(Broken())
        self.assertEqual(report['status'], 'error')
        self.assertFalse(shipped)


if __name__ == '__main__':
    unittest.main()
