UPDATE Parts
SET Name = %(name)s,
PartType = %(parttype)s,
Status = %(status)s,
Remarks = %(remarks)s,
Price = %(price)s
WHERE PartID = %(old_part)s