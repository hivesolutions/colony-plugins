-- copies the name attribute to the card type attribute in the card payment table

-- up
UPDATE CardPayment
   SET card_type = name;

-- down
UPDATE CardPayment
   SET card_type = NULL;
