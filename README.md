# FAERS
Download files from FAERS, and prepare data to import to a Postgresql DB.

**Author**: Allan Ken Miyazono Ushijima
## Requirements

<ul>
    <li>20 GB of storage</li>
    <li>32 GB of memory</li>
    <li>Linux or OS capable of running bash (WSL, MAC). Need the following programs in Linux:</li>
    <li>
        unzip</br>
        To download unzip you need to run the following command: </br>
        <code>sudo apt install unzip </code>
    </li>
    <li>
        wget
    </li>
    <li>
        curl
    </li>
    <li>Necessary libraries: 
        <ul>
            <li>pandas</li>
            <li>numpy</li>
        </ul>
    </li>
</ul>

## Processing

We took the files from 2014 Q3 to 2023 Q4. The reason is to make use of the field "prod_ai" (product active ingredient), and reduce the need to normalize drug names. If there is a need to change the dates, you can modify the variables in download_script_FAERS.sh script (start_year, start_quarter, end_year, end_quarter). 

To steps to run the scripts are: 

<ol>
    <li>
        Change rights to be able to execute the script:</br>
        <code>chmod +x ./download_FAERS.sh ./script_python.sh ./upload_files.sh</code>
    </li>
    <li>
        Run bash script:</br>
        <code>./download_FAERS.sh </code>
    </li>
    <li>
        Run bash script:</br>
        <code>./script_python.sh </code>
    </li>
    <li>
        If you want to host a database with postgresql(please check your server policies like user rights before doing this step):</br>
        <code>sudo -u postgres createdb faers postgres</code>
        <code>sudo -u postgres psql faers < CREATE_TABLE.sql</code></br>
        Change the variables in script upload_files.sh with your database name and user</br>
        <code>./upload_files.sh</code>
    </li>
</ol>

