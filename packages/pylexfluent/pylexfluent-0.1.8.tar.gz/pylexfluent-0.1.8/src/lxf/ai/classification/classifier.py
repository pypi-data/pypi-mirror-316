



import os
import shutil
import logging
from lxf.settings import get_logging_level

###################################################################

logger = logging.getLogger('test classifier')
fh = logging.FileHandler('./logs/test_classifier.log')
fh.setLevel(get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(get_logging_level())
logger.addHandler(fh)
#################################################################



from lxf.ai.classification.multiclass.jupiter_model import MulticlassClassificationJupiterModel
from lxf.ai.ocr.ocr_pdf import do_ocr
from lxf.domain.keyWord import KeyWord
from lxf.domain.keyswordsandphrases import KeysWordsAndPhrases, KeysWordsPhrases
from lxf.domain.predictions import Predictions
from lxf.services.measure_time import measure_time_async
from lxf.services.pdf import get_text_and_tables_from_pdf
from lxf.services.try_safe import try_safe_execute, try_safe_execute_async


from multiprocessing import Process

@measure_time_async
async def get_classification(file_name,max_pages:int=-1) -> Predictions :
    """
    Obtient la classe du fichier fourni en paramètre
    on peut limiter la recherche de la classe du fichier à un certain nombre de pages analysées
    gracee au paramètre max_pages (defaut =-1 cad toutes les pages )
    """
    if os.path.exists(file_name) ==False:
        logger.error(f"Le fichier {file_name} n'existe pas !")
        return None
    result,_ = await try_safe_execute_async(logger,get_text_and_tables_from_pdf, filename=file_name,extract_tables=False,max_pages=max_pages)
    if result==None or result =='':
        # On a rien trouvé en lecture simple du document, essayons avec un OCR 
        output_filename = file_name.replace(".pdf","_ocr.pdf")
        # Pour l'OCR ouvrons un nouveau Process
        p=Process(target=do_ocr,args=(file_name,output_filename))
        p.start()
        p.join(120)
        if os.path.exists(output_filename):
            # Essayons à nouveau de récupérer le texte après OCR
            os.remove(file_name)
            shutil.copy(output_filename, file_name)
            os.remove(output_filename)
            result,_ = await try_safe_execute_async(logger,get_text_and_tables_from_pdf, filename=file_name,extract_tables=False,max_pages=max_pages)


    if result!=None and result!='':
        keysWordsPhrasesHelper:KeysWordsAndPhrases = KeysWordsAndPhrases(result)
        freq_mots= keysWordsPhrasesHelper.get_key_words(isSorted=True, threshold=0.1)
        if freq_mots !=None :
            # convert data to KeysWordsPhrases object 
            result:KeysWordsPhrases = KeysWordsPhrases()
            for mot in freq_mots:
                kword:KeyWord = KeyWord()
                kword.word=mot
                #logger.debug(f"Word: {mot}")
                kword.freq=freq_mots[mot]
                #logger.debug(f"Freq Word: {kword.freq}")
                result.keysWords.append(kword)
            if len(result.keysWords) > 0 :
                jupiter:MulticlassClassificationJupiterModel=MulticlassClassificationJupiterModel()
                pred:Predictions = await  try_safe_execute_async(logger,jupiter.inference,data=result,model_name="jupiter")
                return pred

            else :
                return None
        else :
            return None
    logger.warning("Aucune prediction trouvee")
    return None
            