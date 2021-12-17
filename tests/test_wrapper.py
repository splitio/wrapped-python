import os
import threading

from splitio_wrapper.wrapper import get_factory
from splitio.engine.evaluator import CONTROL


class WrapperTests(object):
    """WrapperTest integration tests."""

    def test_wrapper(self):
        """Instantiate a client with a YAML file and issue get_treatment() calls."""
        filename = os.path.join(os.path.dirname(__file__), 'files', 'splits.yaml')
        factory = get_factory('localhost', config={'splitFile': filename})
        factory.block_until_ready()

        # Evaluations Enabled
        client = factory.client()
        assert client.get_treatment('key', 'my_feature') == 'on'
        assert client.get_treatment_with_config('key', 'my_feature') == ('on', "{\"desc\" : \"this applies only to ON treatment\"}")
        assert client.get_treatments('key', ['my_feature', 'other_feature_2']) == {'my_feature': 'on', 'other_feature_2': 'on'}
        assert client.get_treatments_with_config('key', ['my_feature', 'other_feature_2']) == {'my_feature': ('on', "{\"desc\" : \"this applies only to ON treatment\"}"), 'other_feature_2': ('on', None)}
        assert client.track('key', 'tt', 'event') == None

        manager = factory.manager()
        assert manager.split('my_feature').configs == {
            'on': '{"desc" : "this applies only to ON treatment"}',
            'off': '{"desc" : "this applies only to OFF and only for only_key. The rest will receive ON"}'
        }
        assert len(manager.split_names()) == 4
        assert len(manager.splits()) == 4

        # Evaluations Disabled
        client.disable_evaluations()
        assert client.get_treatment('key', 'other_feature') == CONTROL
        assert client.get_treatment_with_config('key', 'my_feature') == (CONTROL, None)
        assert client.get_treatments('key', ['my_feature', 'other_feature_2']) == {'my_feature': CONTROL, 'other_feature_2': CONTROL}
        assert client.get_treatments_with_config('key', ['my_feature', 'other_feature_2']) == {'my_feature': (CONTROL, None), 'other_feature_2': (CONTROL, None)}
        assert client.track('key', 'tt', 'event') == False

        assert manager.split('my_feature') == None
        assert manager.split_names() == []
        assert len(manager.splits()) == 0

        event = threading.Event()
        factory.destroy(event)
        event.wait()

        # hack to increase isolation and prevent conflicts with other tests
        thread = factory._factory._sync_manager._synchronizer._split_tasks.split_task._task._thread
        if thread is not None and thread.is_alive():
            thread.join()

    def test_wrapper_config(self):
        """Instantiate a client with a YAML file and issue get_treatment() calls."""
        filename = os.path.join(os.path.dirname(__file__), 'files', 'splits.yaml')
        factory = get_factory('localhost', config={'splitFile': filename, 'evaluationsEnabled': True})
        factory.block_until_ready()

        # Evaluations Enabled
        client = factory.client()
        assert client.get_treatment('key', 'my_feature') == 'on'
        assert client.get_treatment_with_config('key', 'my_feature') == ('on', "{\"desc\" : \"this applies only to ON treatment\"}")
        assert client.get_treatments('key', ['my_feature', 'other_feature_2']) == {'my_feature': 'on', 'other_feature_2': 'on'}
        assert client.get_treatments_with_config('key', ['my_feature', 'other_feature_2']) == {'my_feature': ('on', "{\"desc\" : \"this applies only to ON treatment\"}"), 'other_feature_2': ('on', None)}
        assert client.track('key', 'tt', 'event') == None

        manager = factory.manager()
        assert manager.split('my_feature').configs == {
            'on': '{"desc" : "this applies only to ON treatment"}',
            'off': '{"desc" : "this applies only to OFF and only for only_key. The rest will receive ON"}'
        }
        assert len(manager.split_names()) == 4
        assert len(manager.splits()) == 4


        # Evaluations Disabled
        factory2 = get_factory('localhost', config={'splitFile': filename, 'evaluationsEnabled': False})
        factory2.block_until_ready()
        client2 = factory2.client()

        assert client2.get_treatment('key', 'other_feature') == CONTROL
        assert client2.get_treatment_with_config('key', 'my_feature') == (CONTROL, None)
        assert client2.get_treatments('key', ['my_feature', 'other_feature_2']) == {'my_feature': CONTROL, 'other_feature_2': CONTROL}
        assert client2.get_treatments_with_config('key', ['my_feature', 'other_feature_2']) == {'my_feature': (CONTROL, None), 'other_feature_2': (CONTROL, None)}
        assert client2.track('key', 'tt', 'event') == False

        manager2 = factory2.manager()
        assert manager2.split('my_feature') == None
        assert manager2.split_names() == []
        assert len(manager2.splits()) == 0
