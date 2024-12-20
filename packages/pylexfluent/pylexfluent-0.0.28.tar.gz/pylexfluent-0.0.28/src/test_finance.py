import logging
import asyncio
import os
import sys

import lxf.settings as settings
settings.set_logging_level(logging.DEBUG)
settings.enable_tqdm=False
###################################################################

logger = logging.getLogger('test_finance')
fh = logging.FileHandler('./logs/test_finance.log')
fh.setLevel(settings.get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(settings.get_logging_level())
logger.addHandler(fh)
#################################################################


from lxf.domain.loan import Pret
from lxf.extractors.finance import odp_extractor
from lxf.extractors.finance import iban_extractor

from lxf.services.try_safe import  try_safe_execute_async, try_safe_execute_asyncio
from lxf.ai.classification.classifier import get_classification
from lxf.domain.predictions import Predictions
from lxf.services.measure_time import measure_time_async

@measure_time_async
async def do_test_classifier(file_path) -> Predictions :
    """
    """
    return await get_classification(file_name=file_path,max_pages=10)


@measure_time_async
async def do_test_odp(file_path:str)->Pret:
    result = await try_safe_execute_async(logger,odp_extractor.extract_data,file_path=file_path)
    return result
    

async def do_test_iban(file_path:str)->str :
    """
    """
    result = await try_safe_execute_async(logger,iban_extractor.extract_data,file_path=file_path)
    return result

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True) 
    pdf_path = "data/ODP.pdf"
    result = try_safe_execute_asyncio(logger=logger,func=do_test_classifier,file_path=pdf_path) #asyncio.run(do_test(pdf_path))
    print(result)    
    pret:Pret=  try_safe_execute_asyncio(logger,do_test_odp,file_path=pdf_path)
    if pret!=None:
        print(pret.emprunteurs)
    # iban_pdf="data/rib pm.pdf"
    # txt = asyncio.run(do_test_iban(file_path=iban_pdf.encode("utf-8")))
    # print(txt)
    
