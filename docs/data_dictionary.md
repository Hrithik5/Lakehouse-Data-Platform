Data Quality Findings
Validation	Result
Orders → Customers	✅ Passed
Order Items → Orders	✅ Passed
Order Items → Products	✅ Passed
Order Items → Sellers	✅ Passed
Order Payments → Orders	✅ Passed
Order Reviews → Orders	❌ Failed (Source data issue)
Products → Category Translation	❌ Failed (2 missing categories, 13 affected rows)

Then below:

The Olist dataset contains two product categories that do not exist
in the translation table:

- pc_gamer
- portateis_cozinha_e_preparadores_de_alimentos

The pipeline intentionally reports these inconsistencies instead of
silently modifying the source data.

That is a much stronger portfolio story.