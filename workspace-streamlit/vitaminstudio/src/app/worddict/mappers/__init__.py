from sqlalchemy import text
from typing import List

from common.mappers import CommonMapper

from ..schemas.dto.request import WordDictListRequestDto

from ..schemas.vo.cate import WordDictCateVO
from ..schemas.vo.list import WordDictListVO


class WordDictMapper(CommonMapper):
    def __init__(self, db_session):
        super().__init__(db_session)

    def select_word_dict_cate_list(self) -> List[WordDictCateVO]:
        qry_stmt = f'''
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
        qry_result = (self._db_session.execute(text(qry_stmt))).fetchall()

        return self.map_result_to_model(qry_result, WordDictCateVO)

    def select_word_dict_list(self, params: WordDictListRequestDto) -> List[WordDictListVO]:
        qry_stmt = f'''
            /* WordDictMapper.select_word_dict_list */
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
                        and wcd.cate_seq like :cate_seq || case when :cate_seq = '' then '%' else '' end
                        -- 단어 종류
                        and wcd.word_flg_cd like :word_flg_cd  || case when :word_flg_cd is '' then '%' else '' end
                        -- 단어 유형
                        and kwd.kor_word_type_cd like :kor_word_type_cd || case when :kor_word_type_cd is '' then '%' else '' end
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
            limit :paging_display_cnt offset (:paging_display_cnt * (:paging_page_idx - 1))
        '''
        qry_param = {
            'cate_seq': params.cate_seq,
            'word_flg_cd': params.word_flg_cd,
            'kor_word_type_cd': params.kor_word_type_cd,
            'kor_word_nm': params.kor_word_nm,
            'eng_word_nm': params.eng_word_nm,
            'eng_abbr_nm': params.eng_abbr_nm,
            'paging_display_cnt': params.paging_display_cnt,
            'paging_page_idx': params.paging_page_idx
        }

        qry_result = (self._db_session.execute(text(qry_stmt), qry_param)).fetchall()

        return self.map_result_to_model(qry_result, WordDictListVO)
