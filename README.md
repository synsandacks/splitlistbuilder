# splitlistbuilder
 A script to create efficient dynamic-split-tunnel lists for Cisco ASA's. This script adheres to the following conventions:

 - Removes duplicate entries from the split tunnel destinations list.
 - Enforces maximum line attr-value length for the anyconnect-custom-data to 420 chars. [Source](https://www.cisco.com/c/en/us/td/docs/security/asa/asa-cli-reference/A-H/asa-command-ref-A-H/ad-aq-commands.html#wp3141562980)
 - Warns you if the maximum character count for domains exeeds amount allowed by AnyConnect client. In 4.10 and beyond this is 20,000 characters. In versions prior the limit is 5,000 characters. [Source 4.10 and Beyond](https://www.cisco.com/c/en/us/td/docs/security/vpn_client/anyconnect/anyconnect410/administration/guide/b-anyconnect-admin-guide-4-10/configure_vpn.html?bookSearch=true#concept_fly_15q_tz) | [Source 4.9 and Earlier](https://www.cisco.com/c/en/us/td/docs/security/vpn_client/anyconnect/anyconnect49/administration/guide/b_AnyConnect_Administrator_Guide_4-9/configure_vpn.html#concept_fly_15q_tz)
 - Commas are added to the begining of each line with the exception of the first and no line should end in a comma.

# Requirements
This python script is dependant on the PyYAML library. 

Install PyYaml:

    pip install PyYAML

# Usage

	C:\Scripts\splitlistbuilder>python slbuild.py
	What version of AnyConnect do you have deployed?

		[1] AnyConnect 4.10 and Beyond
		[2] AnyConnect 4.9 and Earlier
		[q] Quit

	Please enter a number to specify your AnyConnect client version: 1
	What type of split tunnel list are you building?

		[1] Dynamic Exclude
		[2] Dynamic Include
		[q] Quit

	Please enter a number to specify your split tunnel type: 1
	Please input split tunnel list name: TESTING
	Please select an input option for the split tunnel destinations.

		[1] Paste in comma seperated values
		[2] Load a .txt file
		[3] Load a .yml file
		[q] Quit

	Please input a selection: 3
	Input full path to *.yml file for import or [q] to quit: C:\Scripts\splitlistbuilder\example_lists\urls.yml
	-------------------- Begin Output --------------------
	anyconnect-custom-data dynamic-split-exclude-domains TESTING synsandacks.com,developer.cisco.com,google.com,microsoft.com,github.com,www.python.org,pypi.org,twitter.com,www.cisco.com
	----------------------------------------------------
	[INFO] 1 duplicate entries removed.