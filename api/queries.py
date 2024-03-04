def get_member_kns_query(id_field):
    return f"""
                SELECT
                    f."{id_field}",
                    f."FirstName",
                    f."LastName",
                    f."GenderDesc",
                    f."Email",
                    f."altnames",
                    f."mk_individual_photo",
                    m."faction_name",
                    COALESCE(array_to_string(kns.knesset_array::text[], ', '), '') AS "knesset",
                    COALESCE(json_agg(DISTINCT c."committee_name" || ' (' || c."position_name" || ')') ) AS "committees",
                    CASE WHEN ch."mk_individual_id" IS NOT NULL THEN true ELSE false END AS "IsChairPerson",
                    CONCAT('[', STRING_AGG(DISTINCT CONCAT(year, '-', total_attended_hours), ','), ']') AS year_total_hours_attended
                FROM members_faction_memberships m
                JOIN members_mk_individual f
                    ON f."mk_individual_id" = ANY(ARRAY(SELECT jsonb_array_elements_text(m."member_mk_ids")::integer))
                LEFT JOIN members_mk_individual_committees c
                    ON c."mk_individual_id" = f."mk_individual_id" AND c.finish_date IS NULL
                LEFT JOIN members_mk_individual_faction_chairpersons ch
                    ON ch."mk_individual_id" = f."mk_individual_id"
                LEFT JOIN (
                    SELECT
                        jsonb_array_elements_text(m.member_mk_ids)::integer AS member_mk_id,
                        array_agg(DISTINCT m.knesset) AS knesset_array
                    FROM members_faction_memberships m
                    GROUP BY member_mk_id
                ) kns ON f."mk_individual_id" = kns.member_mk_id
                LEFT JOIN (
                  SELECT members_presence.mk_id, members_presence.year, SUM(members_presence.total_attended_hours) AS total_attended_hours
                  FROM members_presence
                  GROUP BY members_presence.mk_id, members_presence.year
                ) AS members_presence
                ON f."mk_individual_id" = members_presence.mk_id
                WHERE f."{id_field}"=%s
                GROUP BY f."{id_field}", m."faction_name", f."FirstName", f."LastName", f."GenderDesc", f."IsCurrent", f."Email", f."altnames", f."mk_individual_photo", ch."mk_individual_id", kns."knesset_array"
                ORDER BY m."faction_name" DESC
                LIMIT 1;
    """


def get_minister_query(id_field):
    return f"""
                SELECT
                    f."{id_field}",
                    f."FirstName",
                    f."LastName",
                    f."GenderDesc",
                    f."Email",
                    f."altnames",
                    f."mk_individual_photo",
                    mmif."faction_name",
                    CONCAT('[', STRING_AGG(DISTINCT CONCAT(mmig."govministry_name", ': ', mmig."position_name"), ', '),']') AS ministers,
                    CASE WHEN ch."mk_individual_id" IS NOT NULL THEN true ELSE false END AS "IsChairPerson",
                    COALESCE(array_to_string(kns.knesset_array::text[], ', '), '') AS knessets,
                    COALESCE(json_agg(DISTINCT c."committee_name" || ' (' || c."position_name" || ')') ) AS "committees",
                    CONCAT('[', STRING_AGG(DISTINCT CONCAT(year, '-', total_attended_hours), ', '), ']') AS year_total_hours_attended
                FROM members_mk_individual f
                JOIN members_mk_individual_govministries AS mmig
                    ON mmig."mk_individual_id" = f."mk_individual_id"
                LEFT JOIN members_mk_individual_faction_chairpersons ch
                    ON ch."mk_individual_id" = f."mk_individual_id"
                LEFT JOIN (
                    SELECT
                        jsonb_array_elements_text(m.member_mk_ids)::integer AS member_mk_id,
                        array_agg(DISTINCT m.knesset) AS knesset_array
                    FROM members_faction_memberships m
                    GROUP BY member_mk_id
                ) kns ON f."mk_individual_id" = kns.member_mk_id
                LEFT JOIN (
                  SELECT members_presence.mk_id, members_presence.year, SUM(members_presence.total_attended_hours) AS total_attended_hours
                  FROM members_presence
                  GROUP BY members_presence.mk_id, members_presence.year
                ) AS members_presence
                ON f."mk_individual_id" = members_presence.mk_id
                LEFT JOIN members_mk_individual_factions AS mmif
                ON mmif."mk_individual_id"=f."mk_individual_id" and mmif.knesset=(SELECT max(knesset) FROM members_mk_individual_factions) and mmif."faction_name" NOT LIKE '%%נסגרה%%'
                LEFT JOIN members_mk_individual_committees c
                    ON c."mk_individual_id" = f."mk_individual_id" AND c.finish_date IS NULL
                WHERE mmig.finish_date IS NULL AND f."{id_field}"=%s
                GROUP BY f."{id_field}",
                    f."FirstName",
                    f."LastName",
                    f."GenderDesc",
                    f."IsCurrent",
                    f."Email",
                    f."altnames",
                    f."mk_individual_photo",
                    ch."mk_individual_id",
                    kns."knesset_array",
                    mmif."faction_name";
    """


def get_members():
    return """
            SELECT
                members_mk_individual.mk_individual_id,
                members_mk_individual.mk_individual_first_name,
                members_mk_individual.mk_individual_name,
                members_mk_individual."PersonID",
                members_mk_individual."GenderID",
                members_mk_individual."GenderDesc",
                members_mk_individual."IsCurrent",
                members_mk_individual.mk_individual_email,
                members_mk_individual.altnames,
                COALESCE(json_agg(DISTINCT mci.*), '[]') AS committee_positions,
                COALESCE(json_agg(DISTINCT mif.*), '[]') AS factions,
                COALESCE(json_agg(DISTINCT mfcp.*), '[]') AS faction_chairpersons,
                COALESCE(json_agg(DISTINCT migm.*), '[]') AS govministries
            FROM
                members_mk_individual
            LEFT JOIN members_mk_individual_committees mci ON members_mk_individual.mk_individual_id = mci.mk_individual_id AND mci.knesset = %(knesset_term)s
            LEFT JOIN members_mk_individual_factions mif ON members_mk_individual.mk_individual_id = mif.mk_individual_id AND mif.knesset = %(knesset_term)s
            LEFT JOIN members_mk_individual_faction_chairpersons mfcp ON members_mk_individual.mk_individual_id = mfcp.mk_individual_id AND mfcp.knesset = %(knesset_term)s
            LEFT JOIN members_mk_individual_govministries migm ON members_mk_individual.mk_individual_id = migm.mk_individual_id AND migm.knesset = %(knesset_term)s
            WHERE
                members_mk_individual."IsCurrent" = %(is_current)s
            GROUP BY
                members_mk_individual.mk_individual_id, members_mk_individual.mk_individual_first_name,members_mk_individual.mk_individual_name,members_mk_individual."PersonID",members_mk_individual."GenderID"
                ,
                members_mk_individual."GenderDesc",
                members_mk_individual."IsCurrent",
                members_mk_individual.mk_individual_email,
                members_mk_individual.altnames;
    """


def get_member():
    return """
        SELECT
            members_mk_individual.mk_individual_id,
            members_mk_individual.mk_individual_first_name,
            members_mk_individual.mk_individual_name,
            members_mk_individual."PersonID",
            members_mk_individual."GenderID",
            members_mk_individual."GenderDesc",
            members_mk_individual."IsCurrent",
            members_mk_individual.mk_individual_email,
            members_mk_individual.altnames,
            COALESCE(json_agg(DISTINCT mci.*), '[]') AS committee_positions,
            COALESCE(json_agg(DISTINCT mif.*), '[]') AS factions,
            COALESCE(json_agg(DISTINCT mfcp.*), '[]') AS faction_chairpersons,
            COALESCE(json_agg(DISTINCT migm.*), '[]') AS govministries
        FROM
            members_mk_individual
        LEFT JOIN members_mk_individual_committees mci ON members_mk_individual.mk_individual_id = mci.mk_individual_id AND mci.knesset = %(knesset_term)s
        LEFT JOIN members_mk_individual_factions mif ON members_mk_individual.mk_individual_id = mif.mk_individual_id AND mif.knesset = %(knesset_term)s
        LEFT JOIN members_mk_individual_faction_chairpersons mfcp ON members_mk_individual.mk_individual_id = mfcp.mk_individual_id AND mfcp.knesset = %(knesset_term)s
        LEFT JOIN members_mk_individual_govministries migm ON members_mk_individual.mk_individual_id = migm.mk_individual_id AND migm.knesset = %(knesset_term)s
        WHERE
            members_mk_individual."mk_individual_id" = %(mk_individual_id)s
        GROUP BY
            members_mk_individual.mk_individual_id, members_mk_individual.mk_individual_first_name, members_mk_individual.mk_individual_name, members_mk_individual."PersonID", members_mk_individual."GenderID",
            members_mk_individual."GenderDesc", members_mk_individual."IsCurrent", members_mk_individual.mk_individual_email, members_mk_individual.altnames;
    """


def get_members_presence(mk_individual_id: int):
    return f"""select * from members_presence where
            mk_id = {mk_individual_id} order by date desc
    """


def get_members_attended_committee_meetings(mk_individual_id: int):
    return f"""SELECT
                "CommitteeSessionID", "KnessetNum", "TypeID", "TypeDesc",
                "CommitteeID",
                "Location", "SessionUrl", "BroadcastUrl",
                "StartDate", "FinishDate", "Note",
                topics, committee_name, bill_names, bill_types,
                related_to_legislation
            FROM
                people_committees_meeting_attendees
            WHERE
                attended_mk_individual_ids @> '[{mk_individual_id}]'
    """


def get_members_votes(mk_individual_id: int):
    return f"""SELECT * FROM (
                SELECT knesset_num, session_id, sess_item_id, sess_item_dscr, vote_item_id, vote_item_dscr, vote_date, vote_time, is_elctrnc_vote, is_accepted, total_for, total_against, total_abstain, 'pro' AS mk_vote
                FROM votes_view_vote_rslts_hdr_approved_extra
                WHERE mk_ids_pro @> '[{mk_individual_id}]'

                UNION ALL

                SELECT knesset_num, session_id, sess_item_id, sess_item_dscr, vote_item_id, vote_item_dscr, vote_date, vote_time, is_elctrnc_vote, is_accepted, total_for, total_against, total_abstain, 'against' AS mk_vote
                FROM votes_view_vote_rslts_hdr_approved_extra
                WHERE mk_ids_against @> '[{mk_individual_id}]'

                UNION ALL

                SELECT knesset_num, session_id, sess_item_id, sess_item_dscr, vote_item_id, vote_item_dscr, vote_date, vote_time, is_elctrnc_vote, is_accepted, total_for, total_against, total_abstain, 'abstain' AS mk_vote
                FROM votes_view_vote_rslts_hdr_approved_extra
                WHERE mk_ids_abstain @> '[{mk_individual_id}]'
                ) a
    """


def get_members_bills(mk_individual_id: int):
    return f"""SELECT
            bkb."BillID",
            bkb."KnessetNum",
            bkb."Name",
            bkb."SubTypeID",
            bkb."SubTypeDesc",
            bkb."PrivateNumber",
            bkb."CommitteeID",
            bkb."StatusID",
            bkb."Number",
            bkb."PostponementReasonID",
            bkb."PostponementReasonDesc",
            bkb."PublicationDate",
            bkb."MagazineNumber",
            bkb."PageNumber",
            bkb."IsContinuationBill",
            bkb."SummaryLaw",
            bkb."PublicationSeriesID",
            bkb."PublicationSeriesDesc",
            bkb."PublicationSeriesFirstCall",
            bkb_init."IsInitiator"
        FROM
            bills_kns_billinitiator bkb_init
        JOIN
            members_mk_individual mki ON mki."PersonID" = bkb_init."PersonID"
        JOIN
            bills_kns_bill bkb ON bkb."BillID" = bkb_init."BillID"
        WHERE
            mki.mk_individual_id = {mk_individual_id}
    """
