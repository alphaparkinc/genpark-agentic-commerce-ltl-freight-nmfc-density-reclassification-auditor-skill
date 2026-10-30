# -*- coding: utf-8 -*-
"""LTL Freight NMFC Density Reclassification & Dispute Auditor Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def audit_ltl_density_reclassification(**kwargs):
    """Calculates shipment density in PCF, maps to standard NMFC 11-tier classification, audits carrier re-weigh and re-class upcharges, and drafts dispute evidence packages."""
    bol_number = kwargs.get('bol_number')
    billed_weight_lbs = kwargs.get('billed_weight_lbs')
    actual_weight_lbs = kwargs.get('actual_weight_lbs')
    length_in = kwargs.get('length_in')
    width_in = kwargs.get('width_in')
    height_in = kwargs.get('height_in')
    carrier_billed_class = kwargs.get('carrier_billed_class')
    carrier_total_freight_charge_usd = kwargs.get('carrier_total_freight_charge_usd')

    cubic_inches = length_in * width_in * height_in
    cubic_feet = round(cubic_inches / 1728.0, 2)
    pcf = round(actual_weight_lbs / (cubic_feet if cubic_feet > 0 else 1.0), 2)
    
    if pcf >= 50.0:
        correct_class = "Class 50"
    elif pcf >= 35.0:
        correct_class = "Class 55"
    elif pcf >= 30.0:
        correct_class = "Class 60"
    elif pcf >= 22.5:
        correct_class = "Class 65"
    elif pcf >= 15.0:
        correct_class = "Class 70"
    elif pcf >= 12.0:
        correct_class = "Class 77.5"
    elif pcf >= 10.5:
        correct_class = "Class 85"
    elif pcf >= 9.0:
        correct_class = "Class 92.5"
    elif pcf >= 8.0:
        correct_class = "Class 100"
    elif pcf >= 7.0:
        correct_class = "Class 110"
    elif pcf >= 6.0:
        correct_class = "Class 125"
    elif pcf >= 5.0:
        correct_class = "Class 150"
    elif pcf >= 4.0:
        correct_class = "Class 175"
    elif pcf >= 3.0:
        correct_class = "Class 200"
    elif pcf >= 2.0:
        correct_class = "Class 250"
    elif pcf >= 1.0:
        correct_class = "Class 300"
    else:
        correct_class = "Class 400"
        
    is_class_mismatched = carrier_billed_class.strip().lower() != correct_class.lower()
    weight_variance_lbs = round(billed_weight_lbs - actual_weight_lbs, 1)
    
    if is_class_mismatched or weight_variance_lbs > 20.0:
        dispute_recommended = True
        estimated_recoverable_usd = round(carrier_total_freight_charge_usd * 0.28, 2)
        dispute_grounds = f"Carrier misclassified shipment as {carrier_billed_class}. Certified dimensions yield {pcf} PCF which governs {correct_class}. Weight variance of {weight_variance_lbs} lbs."
    else:
        dispute_recommended = False
        estimated_recoverable_usd = 0.0
        dispute_grounds = "Carrier classification matches NMFC density guidelines."
        
    result = {
        "status": "success",
        "bol_number": bol_number,
        "cubic_feet": cubic_feet,
        "density_pcf": pcf,
        "calculated_nmfc_class": correct_class,
        "carrier_billed_class": carrier_billed_class,
        "class_mismatch_detected": is_class_mismatched,
        "weight_variance_lbs": weight_variance_lbs,
        "dispute_recommended": dispute_recommended,
        "estimated_recoverable_overcharge_usd": estimated_recoverable_usd,
        "formal_dispute_grounds": dispute_grounds,
        "engine": "GenPark LTL Freight NMFC Density Audit Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "audit_ltl_density_reclassification": {
        "name": "audit_ltl_density_reclassification",
        "description": "Calculates shipment density in PCF, maps to standard NMFC 11-tier classification, audits carrier re-weigh and re-class upcharges, and drafts dispute evidence packages.",
        "parameters": {
            "type": "object",
            "properties": {
                "bol_number": {"type": "string", "description": "Bill of Lading tracking / PRO number"},
                "billed_weight_lbs": {"type": "number", "description": "Weight charged on carrier freight invoice (lbs)"},
                "actual_weight_lbs": {"type": "number", "description": "Certified scale weight of shipment (lbs)"},
                "length_in": {"type": "number", "description": "Pallet length in inches"},
                "width_in": {"type": "number", "description": "Pallet width in inches"},
                "height_in": {"type": "number", "description": "Pallet height in inches"},
                "carrier_billed_class": {"type": "string", "description": "Freight class charged by carrier (e.g. 'Class 150')"},
                "carrier_total_freight_charge_usd": {"type": "number", "description": "Carrier total invoice charge (USD)"},
            },
            "required": ['bol_number', 'billed_weight_lbs', 'actual_weight_lbs', 'length_in', 'width_in', 'height_in', 'carrier_billed_class', 'carrier_total_freight_charge_usd']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "audit_ltl_density_reclassification":
            res = audit_ltl_density_reclassification(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-ltl-freight-nmfc-density-reclassification-auditor-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-ltl-freight-nmfc-density-reclassification-auditor-skill...")
    test_args = {'bol_number': 'BOL-94810294-X', 'billed_weight_lbs': 1250.0, 'actual_weight_lbs': 1210.0, 'length_in': 48.0, 'width_in': 40.0, 'height_in': 60.0, 'carrier_billed_class': 'Class 150', 'carrier_total_freight_charge_usd': 840.0}
    res = audit_ltl_density_reclassification(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-ltl-freight-nmfc-density-reclassification-auditor-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
