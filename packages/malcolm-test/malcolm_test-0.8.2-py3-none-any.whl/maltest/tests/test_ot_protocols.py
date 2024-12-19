import pytest
import mmguero
import requests
import logging

LOGGER = logging.getLogger(__name__)

UPLOAD_ARTIFACTS = [
    "pcap/protocols/BACnet.pcap",
    "pcap/protocols/BSAP.pcap",
    "pcap/protocols/DNP3.pcap",
    "pcap/protocols/ENIP.pcap",
    "pcap/protocols/ETHERCAT.pcap",
    "pcap/protocols/GENISYS.pcap",
    "pcap/protocols/HARTIP.pcap",
    "pcap/protocols/Modbus.pcap",
    "pcap/protocols/MQTT.pcap",
    "pcap/protocols/OPCUA-Binary.pcap",
    "pcap/protocols/PROFINET.pcap",
    "pcap/protocols/S7comm.pcap",
    "pcap/protocols/Synchrophasor.pcap",
    "pcap/protocols/TDS.pcap",
]

# TODO:
# "ecat_arp_info",
# "ecat_foe_info",
# "ecat_soe_info",
# "ge_srtp",
# "genisys",
EXPECTED_DATASETS = [
    "bacnet",
    "bacnet_device_control",
    "bacnet_discovery",
    "bacnet_property",
    "bestguess",
    "bsap_ip_header",
    "bsap_ip_rdb",
    "bsap_serial_header",
    "bsap_serial_rdb",
    "cip",
    "cip_identity",
    "cip_io",
    "cotp",
    "dnp3",
    "dnp3_control",
    "dnp3_objects",
    "ecat_aoe_info",
    "ecat_coe_info",
    "ecat_dev_info",
    "ecat_log_address",
    "ecat_registers",
    "enip",
    "hart_ip",
    "hart_ip_common_commands",
    "hart_ip_direct_pdu_command",
    "hart_ip_session_record",
    "hart_ip_universal_commands",
    "known_modbus",
    "modbus",
    "modbus_detailed",
    "modbus_mask_write_register",
    "modbus_read_device_identification",
    "modbus_read_write_multiple_registers",
    "mqtt_connect",
    "mqtt_publish",
    "mqtt_subscribe",
    "opcua_binary",
    "opcua_binary_activate_session",
    "opcua_binary_activate_session_locale_id",
    "opcua_binary_browse",
    "opcua_binary_browse_description",
    "opcua_binary_browse_request_continuation_point",
    "opcua_binary_browse_response_references",
    "opcua_binary_browse_result",
    "opcua_binary_close_session",
    "opcua_binary_create_monitored_items",
    "opcua_binary_create_monitored_items_create_item",
    "opcua_binary_create_session",
    "opcua_binary_create_session_discovery",
    "opcua_binary_create_session_endpoints",
    "opcua_binary_create_session_user_token",
    "opcua_binary_create_subscription",
    "opcua_binary_diag_info_detail",
    "opcua_binary_get_endpoints",
    "opcua_binary_get_endpoints_description",
    "opcua_binary_get_endpoints_discovery",
    "opcua_binary_get_endpoints_locale_id",
    "opcua_binary_get_endpoints_profile_uri",
    "opcua_binary_get_endpoints_user_token",
    "opcua_binary_opensecure_channel",
    "opcua_binary_read",
    "opcua_binary_read_nodes_to_read",
    "opcua_binary_read_results",
    "opcua_binary_status_code_detail",
    "opcua_binary_variant_array_dims",
    "opcua_binary_variant_data",
    "opcua_binary_variant_data_value",
    "opcua_binary_variant_extension_object",
    "opcua_binary_variant_metadata",
    "opcua_binary_write",
    "profinet",
    "profinet_io_cm",
    "s7comm",
    "s7comm_plus",
    "s7comm_read_szl",
    "s7comm_upload_download",
    "synchrophasor",
    "synchrophasor_cfg",
    "synchrophasor_cmd",
    "synchrophasor_hdr",
    "tds",
    "tds_rpc",
    "tds_sql_batch",
]


@pytest.mark.mapi
@pytest.mark.pcap
def test_ot_protocols(
    malcolm_http_auth,
    malcolm_url,
    artifact_hash_map,
):
    assert all([artifact_hash_map.get(x, None) for x in mmguero.GetIterable(UPLOAD_ARTIFACTS)])

    response = requests.post(
        f"{malcolm_url}/mapi/agg/event.dataset",
        headers={"Content-Type": "application/json"},
        json={
            "from": "0",
            "filter": {
                "event.provider": "zeek",
                "tags": [artifact_hash_map[x] for x in mmguero.GetIterable(UPLOAD_ARTIFACTS)],
            },
        },
        allow_redirects=True,
        auth=malcolm_http_auth,
        verify=False,
    )
    response.raise_for_status()
    buckets = {
        item['key']: item['doc_count'] for item in mmguero.DeepGet(response.json(), ['event.dataset', 'buckets'], [])
    }
    LOGGER.debug(buckets)
    assert all([(buckets.get(x, 0) > 0) for x in EXPECTED_DATASETS])
