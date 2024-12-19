# [**kiara**](https://dharpa.org/kiara.documentation) plugin: jupyter

This package contains a set of commonly used/useful modules, pipelines, types and metadata schemas for [*Kiara*](https://github.com/DHARPA-project/kiara).

## Description

Jupyter integration for kiara

## Package content

{% for item_type, item_group in get_context_info().get_all_info().items() %}

### {{ item_type }}
{% for item, details in item_group.item_infos.items() %}
- [`{{ item }}`][kiara_info.{{ item_type }}.{{ item }}]: {{ details.documentation.description }}
{% endfor %}
{% endfor %}

## Links

 - Documentation: [https://DHARPA-Project.github.io/kiara_plugin.jupyter](https://DHARPA-Project.github.io/kiara_plugin.jupyter)
 - Code: [https://github.com/DHARPA-Project/kiara_plugin.jupyter](https://github.com/DHARPA-Project/kiara_plugin.jupyter)
