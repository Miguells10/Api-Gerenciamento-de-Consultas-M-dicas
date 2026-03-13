import logging
import uuid

logger = logging.getLogger("apps.appointments")

class AsaasService:
    """
    Service to handle integration with Asaas Payment Gateway.
    Implementing as a mock for now as per requirements.
    """
    
    @staticmethod
    def create_payment(appointment):
        """
        Simulates creating a payment in Asaas with split logic.
        """
        logger.info(f"Simulating Asaas payment creation for Appointment {appointment.id}")
        
        mock_response = {
            "id": f"pay_{uuid.uuid4().hex[:12]}",
            "status": "PENDING",
            "value": 150.00,
            "netValue": 135.00,
            "split": [
                {"walletId": "platform_wallet", "fixedValue": 15.00},
                {"walletId": "professional_wallet", "percentualValue": 90.0}
            ],
            "invoiceUrl": f"https://sandbox.asaas.com/i/{uuid.uuid4().hex[:8]}"
        }
        
        return mock_response

    @staticmethod
    def process_webhook(payload):
        """
        Simulates processing a webhook from Asaas.
        """
        event_type = payload.get("event")
        payment_id = payload.get("payment", {}).get("id")
        
        logger.info(f"Asaas Webhook received: {event_type} for Payment {payment_id}")
        
        if event_type == "PAYMENT_RECEIVED":
            return True
        
        return False
