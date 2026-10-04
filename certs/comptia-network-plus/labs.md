# Network+ Labs

Run these in the Hyper-V lab. Take a checkpoint with the VM powered off before each one.

| Lab | What you do | Objectives |
| --- | --- | --- |
| N-01 Subnet boundaries | Put DC01 at 10.10.20.10/24 and WS01 at 10.10.30.10/24 and show they cannot ping. Change both masks to /16 and show they can. Explain why with the subnet math. | 1.7 |
| N-02 DNS in a domain | On DC01, open DNS Manager and inspect the `lab.local` zone. Add an A record and a PTR record, then resolve both from WS01 with `nslookup`. Compare with the Cloudflare records for johnsontechnicalsystems.com. | 1.4, 3.4 |
| N-03 DHCP | Install the DHCP role on DC01, create a scope, and capture the DORA exchange with `pktmon` or Wireshark when WS01 renews its lease. | 3.4, 5.5 |
| N-04 Ports and services | From WS01, run `Test-NetConnection 10.10.20.10 -Port` for 53, 88, 389, 445, and 3389. On DC01, match each to a listener with `netstat -ano`. | 1.4, 5.5 |
| N-05 Break and fix | Have Claude pick a fault without telling you (wrong DNS server, wrong mask, disabled adapter, wrong gateway). Diagnose it with the seven-step method and write it up in the SOP-003 case format. | 5.1, 5.3 |
| N-06 Routing and VLANs (later) | Add pfSense, route between 10.10.20.0/24 and 10.10.10.0/24, and segment with VLANs as in SOP-005. | 2.1, 2.2 |
