UPDATE Parts
SET Name = %(name)s,
PartType = %(parttype)s,
Status = %(status)s,
Price = %(price)s
WHERE PartID = %(old_part)s