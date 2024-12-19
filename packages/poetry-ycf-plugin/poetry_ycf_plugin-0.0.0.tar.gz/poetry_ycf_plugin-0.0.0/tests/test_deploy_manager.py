from poetry_ycf_plugin.deploy_manager import DeployManager


class TestDeployManager(object):
    def test_init(self, deploy_manager: DeployManager):
        assert deploy_manager

    def test_build(self, deploy_manager: DeployManager):
        assert deploy_manager.build() is None
