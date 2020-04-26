ALTER TABLE after_participant    ADD CONSTRAINT FOREIGN KEY (member_id)       REFERENCES member(id);
ALTER TABLE after_participant    ADD CONSTRAINT FOREIGN KEY (after_id)        REFERENCES after(id);
ALTER TABLE training_participant ADD CONSTRAINT FOREIGN KEY (member_id)       REFERENCES member(id);
ALTER TABLE training_participant ADD CONSTRAINT FOREIGN KEY (training_id)     REFERENCES training(id);
ALTER TABLE result               ADD CONSTRAINT FOREIGN KEY (race_type_id)    REFERENCES race_type(id);
ALTER TABLE result               ADD CONSTRAINT FOREIGN KEY (race_id)         REFERENCES race(id);
ALTER TABLE after                ADD CONSTRAINT FOREIGN KEY (restaurant_id)   REFERENCES restaurant(id);
