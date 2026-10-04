# Security+ Labs

Run these in the Hyper-V lab. Take a checkpoint with the VM powered off before each one.

| Lab | What you do | Objectives |
| --- | --- | --- |
| S-01 Password and lockout policy | Set password and lockout rules in the Default Domain Policy, trigger a lockout from WS01, and find events 4625 (failed logon) and 4740 (account locked out) on DC01. | 1.1, 4.6 |
| S-02 Least privilege | Create a separate admin account and an OU structure (`Build-OUStructure.ps1`). Delegate one task to a non-admin group and test it. | 4.6 |
| S-03 Host firewall by Group Policy | Push a Windows Firewall rule to WS01 by GPO, then prove it with `Test-NetConnection` before and after. | 3.2, 4.5 |
| S-04 Hashing and certificates | Hash an ISO with `Get-FileHash` and compare it with the vendor value. Inspect a certificate's chain, validity dates, and key usage with `certutil`. | 1.4 |
| S-05 Audit logging | Enable advanced audit policy and review events 4624, 4625, and 4720 in the Security log. Write what each tells an investigator. | 4.4, 4.9 |
| S-06 Containment drill | Treat WS01 as compromised and isolate it with `Disconnect-VMNetworkAdapter` on the host, following SOP-006. Record the timeline. | 4.8 |
| S-07 SIEM (later) | Build an Ubuntu Server VM with Wazuh and forward DC01 and WS01 logs. | 4.4 |
