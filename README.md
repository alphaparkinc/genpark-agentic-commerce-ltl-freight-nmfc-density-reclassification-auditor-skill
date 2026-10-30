# LTL Freight NMFC Density Reclassification & Dispute Auditor Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `audit_ltl_density_reclassification`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates shipment density in PCF, maps to standard NMFC 11-tier classification, audits carrier re-weigh and re-class upcharges, and drafts dispute evidence packages.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Logistics / Freight Auditing)`

## MCP Tool Specification
### `audit_ltl_density_reclassification`
Parameters:
- `bol_number` (str): Bill of Lading tracking / PRO number
- `billed_weight_lbs` (float): Weight charged on carrier freight invoice (lbs)
- `actual_weight_lbs` (float): Certified scale weight of shipment (lbs)
- `length_in` (float): Pallet length in inches
- `width_in` (float): Pallet width in inches
- `height_in` (float): Pallet height in inches
- `carrier_billed_class` (str): Freight class charged by carrier (e.g. 'Class 150')
- `carrier_total_freight_charge_usd` (float): Carrier total invoice charge (USD)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-ltl-freight-nmfc-density-reclassification-auditor-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-ltl-freight-nmfc-density-reclassification-auditor-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
