CREATE TABLE person_attributes(
  person_school_id bigint references person_school,
  field varchar,
  value varchar,
  PRIMARY KEY(person_school_id, field)
);
