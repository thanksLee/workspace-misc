--================================================================
-- VitaminStudio - Sample - Query
--================================================================
'''
    Step - 1
    Version : Ver 1.0
    Description :
    - 표준단어 사전 분류를 가져온다.
    Parameter :
'''
select row_number() over(order by a.sort_order) rnum
     , a.cate_nm
     , a.cate_seq
  from ( select 0 sort_order
              , '전체' cate_nm
              , 0 cate_seq
         union all
         select row_number() over(order by coalesce(wc.cate_nm, pj.prj_nm)) sort_order
              , coalesce(wc.cate_nm, pj.prj_nm) cate_nm
              , wc.cate_seq
           from sd_word_cate wc left outer join base_prj pj
                                on pj.prj_seq = wc.prj_seq
         ) a

-- Sample
select row_number() over(order by a.sort_order) rnum
     , a.cate_nm
     , a.cate_seq
  from ( select 0 sort_order
              , '전체' cate_nm
              , 0 cate_seq
         union all
         select row_number() over(order by coalesce(wc.cate_nm, pj.prj_nm)) sort_order
              , coalesce(wc.cate_nm, pj.prj_nm) cate_nm
              , wc.cate_seq
           from sd_word_cate wc left outer join base_prj pj
                                on pj.prj_seq = wc.prj_seq
         ) a

'''
    Step - 2
    Version : Ver 1.0
    Description :
    - 표준 단어사전 리스트를 보여준다.
    Parameter :
    - 01. cate_seq : 분류 일련번호
      02. word_flg_cd : 단어 종류 코드 - ( 1 : 표준단어, 2 : 이음동의어, 3 : 금칙어)
      03. kor_word_type_cd : 단어 유형 코드 - ( 1: 단일어, 2 : 합성어, 3 : 접두어, 4 : 접미어)
      04. kor_wod_nm : 한글 단어 명
      05. eng_word_nm : 영문 단어 명
      06. eng_abbr_nm : 영문 약어 명
      07. paging_display_cnt : 화면에 보여질 개수
      08. paging_page_idx : 현재 페이지 index (0 부터 시작)
'''
select a.rnum
     , a.kor_word_nm
     , ( select x.eng_word_nm
           from sd_eng_word_dict x
          where x.eng_word_seq = a.eng_word_seq
         ) eng_word_nm
     , ( select x.eng_word_nm
           from sd_eng_word_dict x
          where x.eng_word_seq = a.eng_abbr_seq
         ) eng_abbr_nm
     , a.kor_word_type_cd
     , a.word_flg_cd
     , coalesce(a.cate_nm, ( select x.prj_nm
                                from base_prj x
                               where x.prj_seq = a.prj_seq
                             )) cate_nm
     , ( select group_concat(y.term_kor_nm, ', ')
           from sd_term_word_dtl x inner join sd_term_dict y
                                   on y.term_seq = x.term_seq
          where x.kor_word_seq = a.kor_word_seq
            and x.eng_word_seq = a.eng_word_seq
            and x.eng_abbr_seq = a.eng_abbr_seq
            and x.word_flg_cd = a.word_flg_cd
         ) term_kor_nm_list
     , a.total_cnt
     , a.kor_word_seq
     , a.eng_word_seq
     , a.eng_abbr_seq
     , a.cate_seq
  from ( select row_number() over(order by kwd.kor_word_nm) rnum
              , kwd.kor_word_nm
              , kwd.kor_word_type_cd
              , wcd.word_flg_cd
              , wc.cate_nm
              , count(1) over() total_cnt
              , kwd.kor_word_seq
              , kwd.eng_word_seq
              , wcd.eng_abbr_seq
              , wcd.cate_seq
              , wc.prj_seq
           from sd_kor_word_dict kwd inner join sd_word_cate_dtl wcd
                                     on wcd.kor_word_seq = kwd.kor_word_seq
                                     and wcd.eng_word_seq = wcd.eng_word_seq
                                     inner join sd_word_cate wc
                                     on wc.cate_seq = wcd.cate_seq
          where 1 = 1
            -- 분류 필터
            and wcd.cate_seq like :cate_seq || case when :cate_seq is null then '%' else '' end
            -- 단어 종류
            and wcd.word_flg_cd like :word_flg_cd  || case when :word_flg_cd is null then '%' else '' end
            -- 단어 유형
            and kwd.kor_word_type_cd like :kor_word_type_cd || case when :kor_word_type_cd is null then '%' else '' end
            -- 한글명 검색
            and kwd.kor_word_nm like '%'|| :kor_word_nm || '%'
            -- 영문, 약어 명 검색
            and exists ( -- 영문명 검색
                         select 'x'
                           from sd_eng_word_dict x
                          where x.eng_word_seq = kwd.eng_word_seq
                            and x.eng_word_nm like '%'|| :eng_word_nm || '%'
                            and x.p_eng_word_seq is null
                         union all
                         -- 영문 약어 검색
                         select 'x'
                           from sd_eng_word_dict x
                          where x.eng_word_seq = wcd.eng_abbr_seq
                            and x.eng_word_nm like '%'|| :eng_abbr_nm || '%'
                            and x.p_eng_word_seq is not null
                          )
         ) a
 limit :paging_display_cnt offset :paging_page_idx


-- Sample
select a.rnum
     , a.kor_word_nm
     , ( select x.eng_word_nm
           from sd_eng_word_dict x
          where x.eng_word_seq = a.eng_word_seq
         ) eng_word_nm
     , ( select x.eng_word_nm
           from sd_eng_word_dict x
          where x.eng_word_seq = a.eng_abbr_seq
         ) eng_abbr_nm
     , a.kor_word_type_cd
     , a.word_flg_cd
     , coalesce(a.cate_nm, ( select x.prj_nm
                                from base_prj x
                               where x.prj_seq = a.prj_seq
                             )) cate_nm
     , ( select group_concat(y.term_kor_nm, ', ')
           from sd_term_word_dtl x inner join sd_term_dict y
                                   on y.term_seq = x.term_seq
          where x.kor_word_seq = a.kor_word_seq
            and x.eng_word_seq = a.eng_word_seq
            and x.eng_abbr_seq = a.eng_abbr_seq
            and x.word_flg_cd = a.word_flg_cd
         ) term_kor_nm_list
     , a.total_cnt
     , a.kor_word_seq
     , a.eng_word_seq
     , a.eng_abbr_seq
     , a.cate_seq
  from ( select row_number() over(order by kwd.kor_word_nm) rnum
              , kwd.kor_word_nm
              , kwd.kor_word_type_cd
              , wcd.word_flg_cd
              , wc.cate_nm
              , count(1) over() total_cnt
              , kwd.kor_word_seq
              , kwd.eng_word_seq
              , wcd.eng_abbr_seq
              , wcd.cate_seq
              , wc.prj_seq
           from sd_kor_word_dict kwd inner join sd_word_cate_dtl wcd
                                     on wcd.kor_word_seq = kwd.kor_word_seq
                                     and wcd.eng_word_seq = wcd.eng_word_seq
                                     inner join sd_word_cate wc
                                     on wc.cate_seq = wcd.cate_seq
          where 1 = 1
            -- 분류 필터
            and wcd.cate_seq like '' || '%'
            -- 단어 종류
            and wcd.word_flg_cd like '' || '%'
            -- 단어 유형
            and kwd.kor_word_type_cd like '' || '%'
            -- 한글명 검색
            and kwd.kor_word_nm like '%'|| '' || '%'
            -- 영문, 약어 명 검색
            and exists ( -- 영문명 검색
                         select 'x'
                           from sd_eng_word_dict x
                          where x.eng_word_seq = kwd.eng_word_seq
                            and x.eng_word_nm like '%'|| '' || '%'
                            and x.p_eng_word_seq is null
                         union all
                         -- 영문 약어 검색
                         select 'x'
                           from sd_eng_word_dict x
                          where x.eng_word_seq = wcd.eng_abbr_seq
                            and x.eng_word_nm like '%'|| '' || '%'
                            and x.p_eng_word_seq is not null
                          )
         ) a
 limit 20 offset 0