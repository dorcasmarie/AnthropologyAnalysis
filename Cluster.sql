SELECT SPACE.record_id, SPACE.FC1, SPACE.FC2, SPACE.FC3, vv.field_content AS OCLC,
ir.itype_code_num,
irp.call_number, irp.call_number_norm
FROM
(SELECT LEVEL.record_id, LEVEL.FC1, LEVEL.FC2, vv.field_content AS FC3
FROM
(SELECT MAIN.record_id AS record_id, MAIN.field_content AS FC1, varfield_view.field_content AS FC2
FROM
(SELECT varfield_view.record_id, varfield_view.field_content
FROM sierra_view.varfield_view WHERE varfield_view.marc_tag = '050' AND
varfield_view.field_content LIKE '|aGN%') AS MAIN
LEFT JOIN sierra_view.varfield_view ON varfield_view.record_id = MAIN.record_id
WHERE varfield_view.marc_tag = '650') AS LEVEL
LEFT JOIN sierra_view.varfield_view AS vv ON LEVEL.record_id = vv.record_id
WHERE vv.marc_tag = '260') AS SPACE
LEFT JOIN sierra_view.varfield_view AS vv ON SPACE.record_id = vv.record_id
LEFT JOIN sierra_view.bib_record_item_record_link AS brirl on vv.record_id = brirl.bib_record_id
LEFT JOIN sierra_view.item_record AS ir ON brirl.item_record_id = ir.record_id
LEFT JOIN sierra_view.item_record_property AS irp ON ir.record_id = irp.item_record_id
WHERE vv.marc_tag = '001' AND varfield_view.record_type_code = 'i'
