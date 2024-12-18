TEMPLATES = [
    {
        "display_name": "Agent Offline",
        "id": "nc_tmpl:000000001",
        "description": "Send a notification when Spyderbat detects it is no longer receiving data from an Agent (Nano Agent or Clustermonitor, ephemeral or not).",
        "type": "agent_health",
        "config": {
            "schema_type": "event_opsflag",
            "sub_schema": "agent_offline",
            "condition": "",
            "title": "Spyderbat Agent Detected Offline",
            "message": "{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Hostname": "{{ hostname }}",
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Cluster": "{{ __cluster__ }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":red_circle:",
            },
        },
    },
    {
        "display_name": "Agent Back Online",
        "id": "nc_tmpl:000000002",
        "description": "Send a notification when Spyderbat detects that an Agent has come back online and is sending data.",
        "type": "agent_health",
        "config": {
            "schema_type": "event_opsflag",
            "sub_schema": "agent_online",
            "condition": "",
            "title": "Spyderbat Agent Back Online",
            "message": "{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Hostname": "{{ hostname }}",
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Cluster": "{{ __cluster__ }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":large_green_circle:",
            },
        },
    },
    {
        "display_name": "Agent CPU Usage Over Threshold",
        "id": "nc_tmpl:000000003",
        "description": "Send a notification when an Agent's total CPU usage is over 4% for 2 minutes. (30 minute cooldown)",
        "type": "agent_health",
        "config": {
            "schema_type": "event_metric",
            "sub_schema": "agent",
            "condition": "cpu_1min_P.agent > 0.04",
            "for_duration": 120,
            "cooldown": 1800,
            "title": "Spyderbat Agent CPU Over Threshold For 2 Minutes",
            "message": "{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Hostname": "{{ hostname }}",
                    "Cluster": "{{ __cluster__ }}",
                    "CPU Used (%)": "{{ __percent__ | cpu_1min_P.agent }} (Threshold: 4%)",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":large_yellow_circle:",
            },
        },
    },
    {
        "display_name": "Agent Memory Over Threshold",
        "id": "nc_tmpl:000000004",
        "description": "Send a notification when an Agent's memory usage is over 3.5GB for 2 minutes. (30 minute cooldown)",
        "type": "agent_health",
        "config": {
            "schema_type": "event_metric",
            "sub_schema": "agent",
            "condition": "mem_1min_B.agent > 3758096384",
            "for_duration": 120,
            "cooldown": 1800,
            "title": "Spyderbat Agent Memory Usage Over Threshold For 2 Minutes",
            "message": "{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Hostname": "{{ hostname }}",
                    "Cluster": "{{ __cluster__ }}",
                    "Memory Used (%)": "{{ __percent__ | mem_1min_P.agent }}",
                    "Memory Used (bytes)": "{{ mem_1min_B.agent }}B (Threshold: 3.5GB)",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":large_yellow_circle:",
            },
        },
    },
    {
        "display_name": "Agent Bandwidth Over Threshold",
        "id": "nc_tmpl:000000005",
        "description": "Send a notification when an Agent's bandwidth usage is over 125 KBps for 2 minutes. (30 minute cooldown)",
        "type": "agent_health",
        "config": {
            "schema_type": "event_metric",
            "sub_schema": "agent",
            "condition": "bandwidth_1min_Bps > 125000",
            "for_duration": 120,
            "cooldown": 1800,
            "title": "Spyderbat Agent Bandwidth Usage Over Threshold For 2 Minutes",
            "message": "{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Hostname": "{{ hostname }}",
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Cluster": "{{ __cluster__ }}",
                    "Bandwidth Used (Bps)": "{{ bandwidth_1min_Bps }} Bps (Threshold: 125,000 Bps)",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":large_yellow_circle:",
            },
        },
    },
    {
        "display_name": "Bat Offline",
        "id": "nc_tmpl:000000006",
        "description": "Send a notification when a Bat goes offline.",
        "type": "agent_health",
        "config": {
            "schema_type": "event_opsflag",
            "sub_schema": "bat_offline",
            "condition": "",
            "title": "Spyderbat Bat Offline",
            "message": "{{ description }}\n\n{{ __origin__ }}",
            "cooldown": 900,
            "additional_fields": {
                "details": {
                    "Hostname": "{{ hostname }}",
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Bat": "{{ bat_name }}",
                    "Severity": "{{ severity }}",
                    "Cluster": "{{ __cluster__ }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":red_circle:",
            },
        },
    },
    {
        "display_name": "Bat Online",
        "id": "nc_tmpl:000000007",
        "description": "Send a notification when a Bat comes back online.",
        "type": "agent_health",
        "config": {
            "schema_type": "event_opsflag",
            "sub_schema": "bat_online",
            "condition": "",
            "title": "Spyderbat Bat Back Online",
            "message": "{{ description }}\n\n{{ __origin__ }}",
            "cooldown": 900,
            "additional_fields": {
                "details": {
                    "Hostname": "{{ hostname }}",
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Bat": "{{ bat_name }}",
                    "Severity": "{{ severity }}",
                    "Cluster": "{{ __cluster__ }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":large_green_circle:",
            },
        },
    },
    {
        "display_name": "SSH Login Detection",
        "id": "nc_tmpl:000000008",
        "description": "Send a notification when Spyderbat detects an interactive SSH login.",
        "type": "security",
        "config": {
            "schema_type": "event_redflag",
            "sub_schema": "interactive_ssh",
            "condition": "",
            "title": "SSH Login Detected",
            "message": "{{ description }}\n\n{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Time": "{{ __hr_time__ }}",
                    "Source Name": "{{ __source_name__ }}",
                    "Cluster": "{{ __cluster__ }}",
                    "Logged In As": "{{ logged_in_as }}",
                    "From IP": "{{ remote_ip }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":triangular_flag_on_post:",
            },
        },
    },
    # {
    #     "display_name": "Unique Spydertraces",
    #     "id": "nc_tmpl:000000010",
    #     "description": "Send a notification when we see a unique spydertraces. This config is best used when tuning Spyderbat. You can investigate and suppress unique spydertraces to clear up your dashboards. (1 week cooldown per unique spydertrace)",
    #     "type": "security",
    #     "config": {
    #         "schema_type": "model_spydertrace",
    #         "condition": 'suppressed = false AND NOT(trigger_short_name ~= "policy_violation*")',
    #         "cooldown": {
    #             "byField": ["trigger_ancestors", "trigger_class"],
    #             "forSeconds": 604800,
    #         },
    #         "title": "Unique Spydertrace Detected",
    #         "message": "Unique Spydertrace detected. Investigate using the link below and/or suppress via spyctl using:\n"
    #         "```spyctl suppress trace -i {{ id }}```\n"
    #         "\n{{ __origin__ }}\n",
    #         "additional_fields": {
    #             "details": {
    #                 "Time": "{{ __hr_time__ }}",
    #                 "Trigger": "{{ trigger_short_name }}",
    #                 "Trigger Ancestors": "{{ trigger_ancestors }}",
    #                 "Trigger Class": "{{ trigger_class }}",
    #             },
    #             "linkback_text": "View in Spyderbat",
    #             "linkback_url": "{{ __linkback__ }}",
    #             "slack_icon": ":mag_right:",
    #         },
    #     },
    # },
    {
        "display_name": "Guardian Deviation",
        "id": "nc_tmpl:000000009",
        "description": "Send a notification when we see a guardian deviation. (1 hr cooldown per unique deviation)",
        "type": "guardian",
        "config": {
            "schema_type": "event_audit",
            "sub_schema": "guardian_deviation",
            "condition": "",
            "cooldown": {
                "byField": ["policy_uid", "checksum"],
                "forSeconds": 3600,
            },
            "title": "Spyderbat Guardian Deviation Detected",
            "message": 'Record "{{ ref }}" deviated from policy "{{ policy_name }}". To update the policy using Spyctl execute:\n'
            "```spyctl get deviation --policies {{ policy_uid }} {{ id }} -o yaml > deviation.yaml\n"
            "spyctl merge -p {{ policy_uid }} --with-file deviation.yaml```\n"
            "\n{{ __origin__ }}\n",
            "additional_fields": {
                "details": {
                    "Time": "{{ __hr_time__ }}",
                    "Policy": "{{ policy_name }}",
                    "Policy UID": "{{ policy_uid }}",
                    "Policy Mode": "{{ policy_mode }}",
                    "Cluster": "{{ __cluster__ }}",
                    "Hostname": "{{ hostname }}",
                },
                # "linkback_text": "View in Spyderbat",
                # "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":warning:",
            },
        },
    },
    {
        "display_name": "Agent in Error or Critical State",
        "id": "nc_tmpl:000000010",
        "description": "Send a notification when an agent is in error or critical state. (1 day cooldown)",
        "type": "agent_health",
        "config": {
            "schema_type": "model_agent",
            "condition": "status = 'Error' OR status = 'Critical'",
            "cooldown": {
                "byField": ["id", "status"],
                "forSeconds": 86400,
            },
            "title": "Spyderbat Agent in {{ status }} State",
            "message": "This Nano Agent is in a degraded state and may not be sending all necessary data.\n\n{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Hostname": "{{ hostname }}",
                    "Time": "{{ __hr_time__ }}",
                    "Source UID": "{{ muid }}",
                    "Cluster": "{{ __cluster__ }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":warning:",
            },
        },
    },
    {
        "display_name": "Non kubernetes container on kubernetes node",
        "id": "nc_tmpl:000000011",
        "description": "Send a notification when Spyderbat detects an container not managed by kubernetes on a kubernetes node.",
        "type": "security",
        "config": {
            "schema_type": "event_redflag",
            "condition": 'description ~= "A container*not governed by the Kubernetes cluster*"',
            "title": "Non kubernetes container detected on kubernetes node",
            "message": "{{ description }}\n\n{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Time": "{{ __hr_time__ }}",
                    "Source Name": "{{ __source_name__ }}",
                    "Cluster": "{{ __cluster__ }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":triangular_flag_on_post:",
            },
        },
    },
    {
        "display_name": "SSH Login Failure",
        "id": "nc_tmpl:000000012",
        "description": "Send a notification when Spyderbat detects an ssh login failure on a kubernetes node",
        "type": "security",
        "config": {
            "schema_type": "event_redflag",
            "sub_schema": "ssh_failed_login",
            "condition": 'cluster_name ~= "*"',
            "title": "SSH Login Failure Detected",
            "message": "{{ description }}\n\n{{ __origin__ }}",
            "additional_fields": {
                "details": {
                    "Time": "{{ __hr_time__ }}",
                    "User": "{{ user_name }}",
                    "Remote IP": "{{ remote_ip }}",
                    "Source Name": "{{ __source_name__ }}",
                    "Cluster": "{{ __cluster__ }}",
                },
                "linkback_text": "View in Spyderbat",
                "linkback_url": "{{ __linkback__ }}",
                "slack_icon": ":triangular_flag_on_post:",
            },
        },
    },
]
