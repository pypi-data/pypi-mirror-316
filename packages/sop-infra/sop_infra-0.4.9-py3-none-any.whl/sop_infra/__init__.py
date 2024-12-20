from netbox.plugins import PluginConfig


class SopInfraConfig(PluginConfig):
    name = "sop_infra"
    verbose_name = "SOP Infra"
    description = "Manage infrastructure informations of each site"
    version = "0.4.9"
    author = "Leorevoir"
    author_email = "leo.quinzler@epitech.eu"
    base_url = "sop-infra"
    min_version = "4.1.0"


config = SopInfraConfig
