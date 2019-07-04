# Add-on for Defender ATP Hunting Queries in Splunk

## What does this add-on for Splunk do?

It allows you to create queries to onboard the relevant parts of Defender ATP telemetry into Splunk.

## Why does this add-on exist?

1. Defender ATP has a lot of valuable telemetry data that can be used for correlation in Splunk (Enterprise Security).
2. Because Microsoft made their Defender ATP API generally available on 22 April 2019 [https://twitter.com/MsftSecIntel/status/1120381773639143424](https://twitter.com/MsftSecIntel/status/1120381773639143424)
3. There was previously no way to onboard Defender ATP telemetry data into Splunk. 

## Supported Splunk versions and platforms

This add-on works on Linux and Windows

| Splunk version | Linux | Windows
|----------------|-------|---------
| 6.3            | Yes   | Yes
| 6.4            | Yes   | Yes
| 6.5            | Yes   | Yes
| 6.6            | Yes   | Yes
| 7.0            | Yes   | Yes
| 7.1            | Yes   | Yes
| 7.2            | Yes   | Yes
| 7.3            | Yes   | Yes

## How do I install this add-on

### Single instance Splunk deployments

1. In Splunk, click "Manage apps"
2. Click "Browse more apps", search for TA-defender-atp-hunting
3. Install the add-on

### Distributed Splunk deployments

| Instance type | Supported | Required | Description
|---------------|-----------|----------|------------
| Search head   | Yes       | Yes      | Install this add-on on your search head(s) for proper field extraction
| Indexer       | Yes       | No       | This add-on should be installed on a heavy forwarder that does the index time parsing and event breaking. There is no need to install this add-on on an indexer too.
| Universal Forwarder | No  | No       | This add-on is not supported on a Universal Forwarder because it requires Python
| Heavy Forwarder     | Yes | Yes      | Install this add-on on a heavy forwarder

## How do I configure this add-on?

Find the Client ID and Azure AD Tenant ID first in portal.azure.com:

1. In Azure portal go to Azure Active Directory -> App Registrations
2. Go to WindowsDefenderATPThreatIntelAPI
3. Click overview, and find:
   - Application (client) Id 
   - Directory (tenant) Id
4. Create a new Client Secret, see the "How do I configure the Azure side of things"

In Splunk, with all this information you can start to configure a new input in the add-on:

1. Go to Configure, and create a new account. Paste the client id under username, and the client secret under password. Give it a name e.g. client_id_013d1963_d5a9_4329_bc1b_99d8e6db624d
2. Go to inputs and Create a new input:
    - interval: recommended to 900 seconds or greater given the delays in Defender ATP telemetry
    - query: be sure to include a "where"  statement that prevents duplicate events. Example query:

      ````
      ProcessCreationEvents 
      | where EventTime > ago(1200s) and EventTime < ago(300s)
      ````

      Note that the API is rate limited, and also returns max 10000 events to make sure to include extra where clauses to stay below this limit.

## How do I configure the Azure side of things?

1. In Azure portal go to Azure Active Directory -> App Registrations
2. Go to WindowsDefenderATPThreatIntelAPI
3. Under API permissions add "AdvancedQuery.Read.All", and grant admin consent
4. Under Certificates and Secrets add a new Client secret. The secret is only shown once, so make sure to copy to your favourite password manager.



