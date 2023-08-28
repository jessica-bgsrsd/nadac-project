BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "medicamentos" (
	"ndc_description"	TEXT NOT NULL,
	"ndc"	INTEGER NOT NULL,
	"nadac_per_unit"	REAL NOT NULL,
	"effective_date"	TIMESTAMP NOT NULL,
	"pricing_unit"	TEXT NOT NULL,
	"pharmacy_type_indicator"	TEXT NOT NULL,
	"otc"	TEXT NOT NULL,
	"explanation_code"	TEXT NOT NULL,
	"classification_rate_setting"	TEXT NOT NULL,
	"generic_drug_per_unit"	REAL,
	"generic_drug_effective_date"	TIMESTAMP,
	"as_of_date"	TIMESTAMP NOT NULL
);
COMMIT;
