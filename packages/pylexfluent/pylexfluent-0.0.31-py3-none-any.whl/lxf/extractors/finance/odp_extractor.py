
import logging 
from lxf.settings import get_logging_level

###################################################################

logger = logging.getLogger('odp')
fh = logging.FileHandler('./logs/odp.log')
fh.setLevel(get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(get_logging_level())
logger.addHandler(fh)
#################################################################

from lxf.extractors.finance.loans.loan_extractor import LoanDataExtractor
from lxf.services.try_safe import try_safe_execute_async

async def extract_data(**kwargs)->str|None:
    """
    Extrait les données d'une offre de prêt 
    """
    file_path=kwargs.get("file_path",None)
    if file_path==None: 
        logger.error("Extract Data: file_path ne peut pas etre None")
        return None
    logger.debug(f"Demande extraction de donnees pour {file_path}")
    loan:LoanDataExtractor= LoanDataExtractor(file_path)
    result= await try_safe_execute_async(logger,loan.extract_data)
    if result!=None:
        logger.debug(f"Extraction de donnees different de None ? {result!=None}")
    else :
        logger.debug("Extraction retourne aucune donnée")
    return result
