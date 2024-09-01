--==============================================================
-- Table: base_cmn_cd
--==============================================================
create table base_cmn_cd (
key_cd               VARCHAR(3)           not null,
type_cd              VARCHAR(3)           not null,
cd_nm_1              VARCHAR(50)          not null,
cd_nm_2              VARCHAR(100),
use_yn               VARCHAR(1)           not null default 'Y'
      check (use_yn = upper(use_yn)),
dspy_yn              VARCHAR(1)           not null default 'Y'
      check (dspy_yn = upper(dspy_yn)),
sort_order           INTEGER              not null,
reg_dt               DATE                 not null,
mdfy_dt              DATE                 not null,
primary key (key_cd, type_cd)
);

--==============================================================
-- Table: base_user
--==============================================================
create table base_user (
user_id              VARCHAR(20)          not null,
user_nm              VARCHAR(20)          not null,
login_pwd            VARCHAR(512)         not null,
user_type_cd         VARCHAR(1)           not null default '1'
      check (user_type_cd between '1' and '9'),
use_yn               VARCHAR(1)           not null default 'Y'
      check (use_yn = upper(use_yn)),
reg_dt               DATE                 not null,
mdfy_dt              DATE                 not null,
primary key (user_id)
);

--==============================================================
-- Table: base_prj
--==============================================================
create table base_prj (
prj_seq              INTEGER              not null,
prj_nm               VARCHAR(100)         not null,
prj_start_ymd        VARCHAR(8),
prj_end_ymd          VARCHAR(8),
prj_memo             VARCHAR(100),
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (prj_seq),
foreign key (reg_user_id)
      references base_user (user_id),
foreign key (mdfy_user_id)
      references base_user (user_id)
);

--==============================================================
-- Index: idx_prj_01
--==============================================================
create unique index idx_prj_01 on base_prj (
prj_nm ASC
);

--==============================================================
-- Table: sd_domain_dict
--==============================================================
create table sd_domain_dict (
domain_seq           INTEGER              not null,
p_domain_seq         INTEGER,
domain_kor_nm        VARCHAR(50)          not null,
domain_eng_nm        VARCHAR(50),
hrch_lvl             INTEGER              not null default 0,
hrch_sort_order      INTEGER              not null default 1,
domain_memo          VARCHAR(400),
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (domain_seq),
foreign key (p_domain_seq)
      references sd_domain_dict (domain_seq)
);

--==============================================================
-- Table: sd_data_type
--==============================================================
create table sd_data_type (
data_type_seq        INTEGER              not null,
domain_seq           INTEGER,
dbms_type_cd         VARCHAR(2)           not null,
domain_yn            VARCHAR(1)           not null default 'Y'
      check (domain_yn = upper(domain_yn)),
data_type_cd         VARCHAR(3)           not null,
data_type_len        VARCHAR(50),
prcsn_len            VARCHAR(50),
save_memo            VARCHAR(100),
xprsn_memo           VARCHAR(100),
save_unit            VARCHAR(100),
prmsn_val            VARCHAR(100),
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (data_type_seq),
foreign key (domain_seq)
      references sd_domain_dict (domain_seq)
);

--==============================================================
-- Index: uidx_data_type_01
--==============================================================
create unique index uidx_data_type_01 on sd_data_type (
domain_seq ASC,
dbms_type_cd ASC,
domain_yn ASC,
data_type_cd ASC,
data_type_len ASC,
prcsn_len ASC
);

--==============================================================
-- Index: uidx_domain_dict_01
--==============================================================
create unique index uidx_domain_dict_01 on sd_domain_dict (
domain_kor_nm ASC,
domain_eng_nm ASC,
p_domain_seq ASC
);

--==============================================================
-- Table: sd_eng_word_dict
--==============================================================
create table sd_eng_word_dict (
eng_word_seq         INTEGER              not null,
p_eng_word_seq       INTEGER,
eng_word_nm          VARCHAR(100),
eng_word_type_cd     VARCHAR(1)           not null,
use_yn               VARCHAR(1)           not null default 'Y'
      check (use_yn = upper(use_yn)),
hrch_lvl             INTEGER              not null default 0,
hrch_sort_order      INTEGER              not null,
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (eng_word_seq),
foreign key (p_eng_word_seq)
      references sd_eng_word_dict (eng_word_seq)
);

--==============================================================
-- Index: uidx_eng_word_dict_01
--==============================================================
create unique index uidx_eng_word_dict_01 on sd_eng_word_dict (
eng_word_nm ASC,
eng_word_type_cd ASC
);

--==============================================================
-- Table: sd_kor_word_dict
--==============================================================
create table sd_kor_word_dict (
kor_word_seq         INTEGER              not null,
eng_word_seq         INTEGER              not null,
kor_word_nm          VARCHAR(100)         not null,
kor_word_type_cd     VARCHAR(1)           not null default '1',
word_memo            VARCHAR(400),
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (kor_word_seq),
foreign key (eng_word_seq)
      references sd_eng_word_dict (eng_word_seq)
);

--==============================================================
-- Index: uidx_kor_word_dict_01
--==============================================================
create unique index uidx_kor_word_dict_01 on sd_kor_word_dict (
kor_word_nm ASC
);

--==============================================================
-- Table: sd_term_dict
--==============================================================
create table sd_term_dict (
term_seq             INTEGER              not null,
data_type_seq        INTEGER              not null,
term_kor_nm          VARCHAR(50)          not null,
term_eng_nm          VARCHAR(30)          not null,
term_memo            VARCHAR(400),
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (term_seq),
foreign key (data_type_seq)
      references sd_data_type (data_type_seq)
);

--==============================================================
-- Index: uidx_term_dict_01
--==============================================================
create unique index uidx_term_dict_01 on sd_term_dict (
term_kor_nm ASC,
term_eng_nm ASC
);

--==============================================================
-- Table: sd_word_cate
--==============================================================
create table sd_word_cate (
cate_seq             INTEGER              not null,
prj_seq              INTEGER,
cate_nm              VARCHAR(100),
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (cate_seq),
foreign key (prj_seq)
      references base_prj (prj_seq)
);

--==============================================================
-- Table: sd_word_cate_dtl
--==============================================================
create table sd_word_cate_dtl (
kor_word_seq         INTEGER              not null,
eng_word_seq         INTEGER              not null,
eng_abbr_seq         INTEGER              not null,
word_flg_cd          VARCHAR(1)           not null,
cate_seq             INTEGER              not null,
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
mdfy_user_id         VARCHAR(20)          not null,
mdfy_dt              DATE                 not null,
primary key (kor_word_seq, eng_word_seq, eng_abbr_seq, word_flg_cd),
foreign key (cate_seq)
      references sd_word_cate (cate_seq),
foreign key (eng_abbr_seq)
      references sd_eng_word_dict (eng_word_seq),
foreign key (kor_word_seq)
      references sd_kor_word_dict (kor_word_seq),
foreign key (eng_word_seq)
      references sd_eng_word_dict (eng_word_seq)
);

--==============================================================
-- Table: sd_term_word_dtl
--==============================================================
create table sd_term_word_dtl (
term_seq             INTEGER              not null,
kor_word_seq         INTEGER              not null,
eng_word_seq         INTEGER              not null,
eng_abbr_seq         INTEGER              not null,
word_flg_cd          VARCHAR(1)           not null,
reg_user_id          VARCHAR(20)          not null,
reg_dt               DATE                 not null,
primary key (term_seq, kor_word_seq, eng_word_seq, eng_abbr_seq, word_flg_cd),
foreign key (term_seq)
      references sd_term_dict (term_seq),
foreign key (kor_word_seq, eng_word_seq, eng_abbr_seq, word_flg_cd)
      references sd_word_cate_dtl (kor_word_seq, eng_word_seq, eng_abbr_seq, word_flg_cd)
);
