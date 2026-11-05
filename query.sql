
-- Trigger

CREATE FUNCTION reject_quotations_after_sanction()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
UPDATE quotations
SET status='rejected'
WHERE tender_id= NEW.tender_id
AND quotation_id <> NEW.quotation_id 
AND status NOT IN ('withdrawn');

RETURN NEW;
END;
$$;


CREATE TRIGGER trg_reject_other_quotations
AFTER INSERT ON sanctions
FOR EACH ROW
EXECUTE FUNCTION reject_quotations_after_sanction();



-- Stored Procedure

CREATE OR REPLACE PROCEDURE close_expired_tenders()
LANGUAGE plpgsql
AS $$
BEGIN

    UPDATE tenders
    SET status = 'closed'
    WHERE status = 'open'
      AND end_date < CURRENT_DATE;

END;
$$;

