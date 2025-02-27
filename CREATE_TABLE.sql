drop table if exists DEMO;
create table DEMO
(
primaryid varchar not null primary key,
caseid bigint,
caseversion smallint,
i_f_code varchar,
event_dt varchar,
mfr_dt varchar,
init_fda_dt varchar,
fda_dt varchar,
rept_cod varchar,
auth_num varchar,
mfr_num varchar,
mfr_sndr varchar,
lit_ref varchar,
age float4,
age_cod varchar,
age_grp varchar,
sex varchar,
e_sub varchar,
wt varchar,
wt_cod varchar,
rept_dt varchar,
to_mfr varchar,
occp_cod varchar,
reporter_country varchar,
occr_country varchar
);

drop table if exists DRUG;
create table DRUG
(
    primaryid varchar not null,
    caseid bigint,
    drug_seq bigint,
    role_cod varchar,
    drugname varchar,
    prod_ai varchar,
    val_vbm int, 
    route varchar,
    dose_vbm varchar,
    cum_dose_chr float4,
    cum_dose_unit varchar,
    dechal varchar,
    rechal varchar,
    lot_num varchar,
    exp_dt varchar,
    nda_num varchar,
    dose_amt varchar, 
    dose_unit varchar,
    dose_form varchar,
    dose_freq varchar,
CONSTRAINT primaryid
    FOREIGN KEY(primaryid) 
    REFERENCES demo(primaryid));

drop table if exists INDI;
create table INDI
(
    primaryid varchar not null,
    caseid bigint,
    indi_drug_seq int, 
    indi_pt varchar,
CONSTRAINT primaryid
    FOREIGN KEY(primaryid) 
    REFERENCES demo(primaryid));

drop table if exists OUTC;
create table OUTC
(
    primaryid varchar not null,
    caseid bigint,
    outc_cod varchar,
CONSTRAINT primaryid
    FOREIGN KEY(primaryid) 
    REFERENCES demo(primaryid)
);


drop table if exists REAC;
create table REAC
(
    primaryid varchar not null,
    caseid bigint,
    pt varchar, 
    drug_rec_act varchar,
CONSTRAINT primaryid
    FOREIGN KEY(primaryid) 
    REFERENCES demo(primaryid));

drop table if exists RPSR;
create table RPSR
(
    primaryid varchar not null,
    caseid bigint,
    rpsr_cod varchar,
CONSTRAINT primaryid
    FOREIGN KEY(primaryid) 
    REFERENCES demo(primaryid)
);


drop table if exists RPSR;
create table RPSR
(
    primaryid varchar not null,
    caseid bigint,
    rpsr_cod varchar,
CONSTRAINT primaryid
    FOREIGN KEY(primaryid) 
    REFERENCES demo(primaryid)
);


drop table if exists THER;
create table THER
(
    primaryid varchar not null,
    caseid bigint,
    dsg_drug_seq bigint,
    start_dt varchar,
    end_dt varchar,
    dur varchar,
    dur_cod varchar,
CONSTRAINT primaryid
    FOREIGN KEY(primaryid) 
    REFERENCES demo(primaryid)
);


