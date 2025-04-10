# FAERS
The purpose of this repository is the following: 
<ul>
    <li>Download files from FAERS, and prepare data to import to a Postgresql DB.</li>
    <li>Obtain PRR of a specific group of drugs like antidepressants, either <b>local</b> values (comparing only with the specified group, example prr compared to only antidepressants), or <b>global</b> values (comparing with all the drugs of FAERS.</li>
</ul>
<b>Author</b> : Allan Ken Miyazono Ushijima </br>
<b>email</b> : allan.miyazono@gmail.com
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
            <li>polars (v2)</li>
            <li>pandas</li>
            <li>numpy</li>
        </ul>
    </li>
</ul>

## Versions
<ol>
    <li><b>v1</b>: Used data obtained in February 2024, and we only considered this scripts to clean data and upload it to postgresql</li>
    <li><b>v2</b>: To allow people to access the data without Postgresql, we used polars to obtain PRR (prr_polars). As we use polars the processing time is shorter that with the script sql_prr.py</li>
</ol>

## Processing

We took the files from 2014 Q3 to 2024 Q4 (v2). The reason is to make use of the field "prod_ai" (product active ingredient), and reduce the need to normalize drug names. If there is a need to change the dates, you can modify the variables in download_script_FAERS.sh script (start_year, start_quarter, end_year, end_quarter). 

To steps to run the scripts are: 

<ol>
    <li>Create conda environment. </br>
        <code>conda env create --file environment.yml</code>
    </li>
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
        <code>sudo -u postgres createdb faers postgres</code></br>
        <code>sudo -u postgres psql faers < CREATE_TABLE.sql</code></br>
        Change the variables in script upload_files.sh with your database name and user</br>
        <code>./upload_files.sh</code>
    </li>   
    <li>
        To obtain the prr of the group of drugs, update Drugs.csv</br>
        <code>nano Drugs.csv</code>
    </li>   
    <li>
        Run polars script to obtain prr</br>
        <code>python prr_polars.py</code>
    </li>
</ol>

## Limitations

There are some limitations to our approach, as we only modified the data to be able to obtain the PRR. The limitations that we found are the following:
<ul>
    <li>The dates cannot be parsed automatically as they are considering different formats: YYYYMMDD, YYYYMM, and YYYY. We didn't process this field to prevent increasing the memory and storage (by dividing them into year, month and day; and parsing the full dates in another column). </li>
    <li>In DEMO, the units of ages are varied. There are some rows that have entries of a person above the age of 30 years old with units of days or months.</li>
    <li>In DEMO, the units of weight/mass are varied, and cannot be processed directly. Some of the rows have the unit of mass (example: 70 KG), so it is necessary to first obtain the float and then convert it to required units of mass.</li>
</ul>

