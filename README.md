## Workflow

[Getting your API](https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key)

To Start working with the Palo Alto API, we'll need to create an API key from an existing username and password. This action is only performed once and will only return the key once so make sure to capture the response. Treat your API key like a password.

```
curl -k -X GET 'https://10.222.2.1/api/?type=keygen&user=apiguy&password=apiguypassword' 
```

This get requests sends a username and password and returns with a an API key that we'll use for remaining requests.

```
<response status = 'success'>
    <result>
         <key>LUFRPT00aG1Lc0R2cEdpNWlPVi94WlhSckFqTUJVck09TU5JdDBFcVlsWjdSODVXZGhkc2RXT0YvclN4VlNzdTJnVG9nYWdNUUhJSDFLMzhoWjRzYjVXOEIrU1IzUXBISg==</key>
    </result>
</response> 
```

## EXAMPLE 1: Retrieve Firewall System Info

Grab system info from Palo using header auth

```
curl -H "X-PAN-KEY: LUFRPT00aG1Lc0R2cEdpNWlPVi94WlhSckFqTUJVck09TU5JdDBFcVlsWjdSODVXZGhkc2RXT0YvclN4VlNzdTJnVG9nYWdNUUhJSDFLMzhoWjRzYjVXOEIrU1IzUXBISg==" -k 'https://10.222.2.1/api/?type=op&cmd=<show><system><info></info></system></show>' 
```

If everything is working correctly, we'll get infomation similar to the following:

```
<response status="success"><result><system>
    <hostname>Cyber-Range-Edge</hostname>
    <ip-address>...
    ...<time>Wed Jun 22 20:02:46 2022</time>
    <uptime>18 days, 20:47:04</uptime>
    <devicename>Cyber-Range-Edge</devicename>
    <family>220</family>
    <model>PA-220</model>...<truncated> 
```

## EXAMPLE 2: Backup a Running-config

[Knowledge Base Article](https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000Cm7yCAC)

Pull the config using the API

```
curl -kG "https://10.222.2.1/api/?type=export&category=configuration&key=LUFRPT00aG1Lc0R2cEdpNWlPVi94WlhSckFqTUJVck09TU5JdDBFcVlsWjdSODVXZGhkc2RXT0YvclN4VlNzdTJnVG9nYWdNUUhJSDFLMzhoWjRzYjVXOEIrU1IzUXBISg==" 
```

This will return the running-config directly to the terminal:

```
<config version="10.1.0" urldb="paloaltonetworks" detail-version="10.1.0"><mgt-config><users>...<truncated> 
```

Let's run the same command and route the output to a file. It's recommended to include the date the backup was pulled in the filename.

```
curl -kG "https://10.222.2.1/api/?type=export&category=configuration&key=LUFRPT00aG1Lc0R2cEdpNWlPVi94WlhSckFqTUJVck09TU5JdDBFcVlsWjdSODVXZGhkc2RXT0YvclN4VlNzdTJnVG9nYWdNUUhJSDFLMzhoWjRzYjVXOEIrU1IzUXBISg==" > 6-6-22-running-config.xml 
```

Adding "> 6-6-22-running-config.xml" to the end of the curl request redirects standard output to the file 6-6-22-running-config.xml. If all went smoothly, this file is a working running-config backup. It should be treated with care, as it can contain certificates, keys, usernames, password hashes and other configuration details.

## EXAMPLE 3: INVESTIGATE AN ASSET (unknown device)


![](images/workflow.png)

### Review Workflow

Reviewing logs and alerts, you may encounter a device that you do not recognize. This workflow can help us passively learn more about the device without disrupting, blocking or attempting to connect to it.

1.  Starting with either a suspicious MAC address or a suspicious IP address, we'll want to find the remaining variable. MAC addresses will be most helpful with devices that are Layer 2 adjacent (not connected through another router). 

2.  We can use API queries to search the DHCP entries in the system log and look at the active ARP table to map IP and MAC addresses from the firewalls perspective.

3.  Who makes this device? We can use an API to query a public directory of MAC addresses and with the MAC address and see what type of device it's registered as.

3.  DHCP logs

4. We can look at traffic logs  and threat logs and examine host behaviors

### TRAFFIC LOGS

**Where is traffic going?**
Destination address?
Destination region?
Application (or ports/protocol)?

### THREAT LOGS

Any threat events triggered?

Timeline - (what is it and how long has it been there)
MAC vendor lookup
curl https://api.macvendors.com/FC-A1-3E-2A-1C-33
Poll DHCP log via API (retrieve logs)
https://docs.paloaltonetworks.com/pan-os/10-1/pan-os-panorama-api/pan-os-xml-api-request-types/retrieve-logs-api

DHCP Query:

`https://$HOSTIP/api/?type=log&log-type=system&query=(%20subtype%20eq%20dhcp%20)`

Grab Job ID:

`https://<hostname>/api/?type=log&action=get&job-id=185`

TRAFFIC LOGS




Retreive a PCAP from the Firewall

https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/export-files-api/export-packet-captures/export-threat-filter-and-data-filtering-pcaps#id132daa4d-1a0d-4603-829d-aca09850dc78

