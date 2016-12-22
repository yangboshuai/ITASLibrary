import random
from robot.api import logger

from APEXLibrary._global import _GloableKeywords,_globalVariables
from _itasGlobalVariables import _itasGlobalVariables
from _itasTestData import newRegisterData,approveRegisterData,completeRegisterData

class _REGKeywords(object):
    '''ITAS REG library'''

    def __init__(self):
        '''init function'''
        pass

    def newRegister(self,newRegisterData):
        '''new a register request
        :return string'''

        def getBizKey():
            '''get Biz Key'''

            path = '/ITAS/UserFlow/getBizKey.do'
            query = 'axPrefix=&axType=SEQ_TREG07_TAXPAYER_REQUEST&axBizTaskId=undefined&r=' + str(random.random())
            bizKeyUrl = _globalVariables.BASEURL + path + '?' + query
            logger.info('bizKeyUrl:' + bizKeyUrl, also_console=True)

            bizKeyResp = _globalVariables.SESSION.get(bizKeyUrl)

            logger.info('get biz Key:'+bizKeyResp.text,also_console=True)
            return bizKeyResp.text

        requestUID=getBizKey()
        logger.info('requestUID:',requestUID)
        _itasGlobalVariables.REQUESTUID=requestUID

        path='/ITAS/UserFlow/start.do'
        query='axBizProcDefiId=RegistrationTaxpayerProcess&axBizkey='+requestUID+'&r=' +str(random.random())+\
              '&axBizIsNew=true&axBizIsFlow=true&axBizFlowAction=submit&axBizEntityType=com.cacss.itas.reg.entity.Taxpayer'
        newRegisterUrl=_globalVariables.BASEURL+path+'?'+query
        logger.info('newRegisterUrl:'+newRegisterUrl,also_console=True)

        newRegisterResp=_globalVariables.SESSION.post(newRegisterUrl,newRegisterData)
        logger.info('firstName:'+newRegisterData['treg00NaturalPerson.creg00FirstName'],also_console=True)
        logger.info('lastName:'+newRegisterData['treg00NaturalPerson.creg00LastName'],also_console=True)
        logger.info('idNum:'+newRegisterData['treg00NaturalPerson.creg00IdNo'],also_console=True)
        logger.info('post new register request done.',also_console=True)
        return newRegisterResp.text

    def isRegisterSubmitSuccess(self,newRegisterResp):
        '''check if submit new register successfully
        :return true|false'''

        if 'true' in newRegisterResp:
            logger.info('submit new register successfully:'+newRegisterResp,also_console=True)
            return True
        else:
            logger.error('submit new register failed:'+newRegisterResp)
            return False

    def searchRegister(self,searchRequestUID=''):
        '''search register,default:all
        :return a dict object'''

        path='/ITAS/reg/registration/request/search.do'
        searchRegisterUrl=_globalVariables.BASEURL+path

        searchRegisterData={'axgridid':'gridview',
                            'gridview_startIndex':0,
                            'gridview_pageSize':10,
                            'gridview_sort':'',
                            '':'',
                            'searchStartDate_q':'',
                            'searchStartDate_h':'',
                            'creg08Applicant':'',
                            'creg08SubmitSrc':'',
                            'creg08Status':'',
                            'creg08CaptureOfficerName':'',
                            'creg08IdNumber':'',
                            'creg08RequestUid':searchRequestUID,
                            'creg08ActionDateFrom':'',
                            'creg08ActionDateTo':'',
                            'axgrid_listcols':'creg08RequestDate,creg08Applicant,creg08SubmitSrc,creg08Status,creg08CaptureOfficerName,creg08IdNumber,creg08ActionDate'

                            }

        searchRegisterResp=_globalVariables.SESSION.post(searchRegisterUrl,searchRegisterData)
        logger.info('send search register request done.',also_console=True)

        searchRegisterRespText=searchRegisterResp.text

        convertResult=_GloableKeywords.parseRespToDictOrCuple(searchRegisterRespText)

        if isinstance(convertResult,tuple):
            '''if searchRegisterTmp2 is tuple
            return frist one'''

            logger.info('get more than one row,get the first row.',also_console=True)
            return convertResult[0]
        else:
            return convertResult

    def approveRegister(self,approveUid):
        '''approve register
        :param approveUid
        :return true or false'''

        '''/ITAS/reg/registration/request/listPage.do
        get current userid'''
        path = '/ITAS/reg/registration/request/listPage.do'
        listPageUrl=_globalVariables.BASEURL+path
        listPageResp = _globalVariables.SESSION.get(listPageUrl)

        rightBoundary='currentUserUid\" value=\''
        leftBoundary = '\'/>'
        currentUserUid=_GloableKeywords.subString(listPageResp.text,rightBoundary,leftBoundary)


        '''search data'''
        searchDict=self.searchRegister(approveUid)
        logger.info('searh approveUid result:',searchDict)


        approveRegisterData['parameter.requestUid']=searchDict['creg08RequestUid']
        approveRegisterData['taxpayerRequest.creg07RequestUid']=searchDict['creg08RequestUid']
        approveRegisterData['registrationRequest.creg08RequestUid'] = searchDict['creg08RequestUid']
        approveRegisterData['registrationRequest.creg08RequestDate']=searchDict['creg08RequestDate']
        approveRegisterData['registrationRequest.creg08CaptureOfficer']=searchDict['creg08CaptureOfficer']
        approveRegisterData['oldIdNumber'] = searchDict['creg08IdNumber']
        approveRegisterData['treg00NaturalPerson.creg00IdNo'] = searchDict['creg08IdNumber']
        approveRegisterData['registrationRequest.creg08Applicant'] = searchDict['creg08Applicant']
        axBizProcInstId=searchDict['creg08AxBizTaskId']

        '''/ITAS/reg/registration/request/process.do'''
        path = '/ITAS/reg/registration/request/process.do'
        query ='axBizBackUrl=/ITAS/reg/registration/request/listPage.do' \
               '&axBizViewFlowFormPageUrl=com/cacss/itas/reg/registration.edit' \
               '&requestType=TXP_REG&requestUid='+approveUid+'&requestStatus=SUBMITTED' \
               '&axBizProcInstId='+axBizProcInstId+'&currentUserUid='+currentUserUid +\
               '&rnd='+str(random.random())

        processUrl=_globalVariables.BASEURL+path+'?'+query
        processResp = _globalVariables.SESSION.post(processUrl)

        leftBoundary='var reqProcId = "'
        rightBoundary='";'
        axBizTaskId=_GloableKeywords.subString(processResp.text,leftBoundary,rightBoundary)


        '''taxtype data'''
        path = '/ITAS/reg/taxtype/config.do'
        query = 'taxpayerCategory=IND&taxpayerType=INDSP&requestUid='+approveUid+'&branchUid=&requestStatus=SUBMITTED&requestType=TXP_REG'
        configTaxTypeUrl=_globalVariables.BASEURL+path+'?'+query
        configTaxTypeData={'axgrid_listcols':'cret09TaxTypeName,registeredTaxType.creg06EffectiveDate,registeredTaxType.creg06Fin,registeredTaxType.creg06Status,registeredTaxType.taxpayer.creg06IsRegular,registeredTaxType.creg06ExpiryDate,registeredTaxType.taxpayer.functions',
                           'axgridid':'taxtypeview',
                           'taxtypeview_pageSize':10,
                           'taxtypeview_sort':'',
                           'taxtypeview_startIndex':0}
        configTaxTypeResp = _globalVariables.SESSION.post(configTaxTypeUrl, configTaxTypeData)

        logger.debug('configTaxTypeResp.text'+configTaxTypeResp.text)

        convertResult=_GloableKeywords.parseRespToDictOrCuple(configTaxTypeResp.text)
        approveRegisterData['registeredTaxType[0].cret09TaxtypeUid']= convertResult['cret09TaxtypeUid']
        approveRegisterData['registeredTaxType[0].creg06EffectiveDate']= convertResult['registeredTaxType']['creg06EffectiveDate']


        '''attachment data'''
        path = '/ITAS/reg/attachment/list.do'
        query = 'entityId='+approveUid+'&attachmentTable=TREG05_ATTACHMENT&requestUid='+approveUid+\
                '&requestStatus=SUBMITTED&requestType=TXP_REG&taxpayerCategory=TAXPAYER_TYPE,ID_TYPE,TAX_TYPE'
        attachmentTaxTypeUrl=_globalVariables.BASEURL+path+'?'+query
        attachmentTypeData={'attachmentview_pageSize':10,
                           'attachmentview_sort':'',
                           'attachmentview_startIndex':0,
                           'axgrid_listcols':'ccmn00DocumentTypecode,ccmn00IsUpload,ccmn00UploadDate,ccmn00Note,ccmn00ArchivedDate',
                           'axgridid':'attachmentview'}
        attachmentTypeResp = _globalVariables.SESSION.post(attachmentTaxTypeUrl, attachmentTypeData)

        attachmentResult=_GloableKeywords.parseRespToDictOrCuple(attachmentTypeResp.text)
        for i in range(len(attachmentResult)):
            approveRegisterData['attachments['+str(i)+'].ccmn00IsUpload']=attachmentResult[i]['ccmn00IsUpload']
            approveRegisterData['attachments['+str(i)+'].ccmn00Barcode']=attachmentResult[i]['ccmn00Barcode']
            approveRegisterData['attachments['+str(i)+'].ccmn00AttachUid']=attachmentResult[i]['ccmn00AttachUid']
            approveRegisterData['attachments['+str(i)+'].ccmn00DocumentTypecode']=attachmentResult[i]['ccmn00DocumentTypecode']
            approveRegisterData['attachments['+str(i)+'].ccmn00Entity']=attachmentResult[i]['ccmn00Entity']
            approveRegisterData['attachments['+str(i)+'].mandatory'] = attachmentResult[i]['mandatory']
            approveRegisterData['attachments['+str(i)+'].ccmn00IsConf'] = attachmentResult[i]['ccmn00IsConf']
            approveRegisterData['attachments['+str(i)+'].ccmn00UploadDate'] = attachmentResult[i]['ccmn00UploadDate']
            approveRegisterData['attachments['+str(i)+'].ccmn00ArchivedDate'] = attachmentResult[i]['ccmn00ArchivedDate']


        '''account data'''
        path = '/ITAS/reg/account/list.do'
        query = 'taxpayerUid=&requestStatus=SUBMITTED&requestType=TXP_REG&requestUid='+approveUid
        accountUrl=_globalVariables.BASEURL+path+'?'+query
        accountData={'accountview_pageSize':10,
                     'accountview_sort':'',
                     'accountview_startIndex':0,
                    'axgrid_listcols':'creg04BankName,creg04BranchName,creg04BranchNo,creg04AccountType,creg04AccountNo,creg04Holder,creg04IsShared',
                    'axgridid':'accountview'}
        accountResp = _globalVariables.SESSION.post(accountUrl, accountData)

        accountResult = _GloableKeywords.parseRespToDictOrCuple(accountResp.text)
        approveRegisterData['accounts[0].creg04AccountNo'] = accountResult['creg04AccountNo']
        approveRegisterData['accounts[0].creg04Holder'] = accountResult['creg04Holder']
        approveRegisterData['accounts[0].creg04BankName'] = accountResult['creg04BankName']
        approveRegisterData['accounts[0].creg04AccountType'] = accountResult['creg04AccountType']
        approveRegisterData['accounts[0].creg04BranchName'] = accountResult['creg04BranchName']
        approveRegisterData['accounts[0].creg04BranchNo'] = accountResult['creg04BranchNo']
        approveRegisterData['oldFirstName'] = accountResult['creg04Holder']
        approveRegisterData['parameter.account_holder_name'] = accountResult['creg04Holder']
        approveRegisterData['treg00NaturalPerson.creg00FirstName'] = accountResult['creg04Holder']
        approveRegisterData['treg00NaturalPerson.creg00Email'] = accountResult['creg04Holder']+'@qq.com'

        '''deal with lastname'''
        approveRegisterData['oldLastName'] = searchDict['creg08Applicant'].split(accountResult['creg04Holder'])[1][1:]
        approveRegisterData['treg00NaturalPerson.creg00LastName'] = searchDict['creg08Applicant'].split(accountResult['creg04Holder'])[1][1:]



        path = '/ITAS/UserFlow/submit.do'
        query = 'axBizIsNew=false&axBizIsFlow=true&axBizFlowAction=approve&axBizTaskId='+axBizTaskId+ \
                '&axBizEntityType=com.cacss.itas.reg.entity.Taxpayer'
        approveUrl=_globalVariables.BASEURL+path+'?'+query
        approveResp = _globalVariables.SESSION.post(approveUrl, approveRegisterData)

        path = '/ITAS/reg/refresh/taxpayer.do'
        taxpayerData={'requestID':'',
                     'tin':'',
                     'flag':0,
                    'entityFlag':'1',
                    'sid':approveUid}
        taxpayerUrl=_globalVariables.BASEURL+path
        taxpayerResp = _globalVariables.SESSION.post(taxpayerUrl, taxpayerData)

        path = '/ITAS/reg/call/callRETPort.do'
        callRETPortData={'requestID':approveUid,
                     'requestType':'TXP_REG',
                    }
        callRETPortUrl=_globalVariables.BASEURL+path
        callRETPortResp = _globalVariables.SESSION.post(callRETPortUrl, callRETPortData)

        return approveResp.text

    def isApproveRegisterSuccess(self,approveRegisterResp):
        '''check if approve register successfully
        :return true|false'''

        if 'true' in approveRegisterResp:
            logger.info('approve register successfully:'+approveRegisterResp,also_console=True)
            return True
        else:
            logger.error('approve register failed:'+approveRegisterResp)
            return False

    def completeRegister(self,completeUid):
        '''complete register key worlds
        :param completeUid
        :return completeRegisterResp'''

        '''/ITAS/reg/registration/request/listPage.do
        get current userid'''

        path = '/ITAS/reg/registration/request/listPage.do'
        listPageUrl=_globalVariables.BASEURL+path
        listPageResp = _globalVariables.SESSION.get(listPageUrl)

        rightBoundary='currentUserUid\" value=\''
        leftBoundary = '\'/>'
        currentUserUid=_GloableKeywords.subString(listPageResp.text,rightBoundary,leftBoundary)


        '''search data'''
        searchDict=self.searchRegister(completeUid)

        completeRegisterData['parameter.requestUid']=searchDict['creg08RequestUid']
        completeRegisterData['taxpayerRequest.creg07RequestUid']=searchDict['creg08RequestUid']
        completeRegisterData['registrationRequest.creg08RequestUid'] = searchDict['creg08RequestUid']
        completeRegisterData['registrationRequest.creg08RequestDate']=searchDict['creg08RequestDate']
        completeRegisterData['registrationRequest.creg08CaptureOfficer']=searchDict['creg08CaptureOfficer']
        completeRegisterData['oldIdNumber'] = searchDict['creg08IdNumber']
        completeRegisterData['treg00NaturalPerson.creg00IdNo'] = searchDict['creg08IdNumber']
        completeRegisterData['registrationRequest.creg08Applicant'] = searchDict['creg08Applicant']
        axBizProcInstId=searchDict['creg08AxBizTaskId']

        '''/ITAS/reg/registration/request/process.do'''

        path = '/ITAS/reg/registration/request/process.do'
        query ='axBizBackUrl=/ITAS/reg/registration/request/listPage.do' \
               '&axBizViewFlowFormPageUrl=com/cacss/itas/reg/registration.edit' \
               '&requestType=TXP_REG&requestUid='+completeUid+'&requestStatus=APPROVED' \
               '&axBizProcInstId='+axBizProcInstId+'&currentUserUid='+currentUserUid +\
               '&rnd='+str(random.random())

        processUrl=_globalVariables.BASEURL+path+'?'+query
        processResp = _globalVariables.SESSION.post(processUrl)
        leftBoundary='var reqProcId = "'
        rightBoundary='";'
        axBizTaskId=_GloableKeywords.subString(processResp.text,leftBoundary,rightBoundary)
        completeRegisterData['treg02Individual.creg02IndividualUid']=_GloableKeywords.subString(processResp.text,'creg02IndividualUid" value="','" />')
        completeRegisterData['treg00NaturalPerson.creg00NaturalPersonUid'] = _GloableKeywords.subString(processResp.text,
                                                                                          'creg02IndividualUid" value="',
                                                                                          '" />')
        completeRegisterData['postalAddress.creg26AddressUid'] = _GloableKeywords.subString(processResp.text,
                                                                                          'postalAddress.creg26AddressUid" value="',
                                                                                          '"/>')
        completeRegisterData['parameter.creg01Tin'] = _GloableKeywords.subString(processResp.text,
                                                                                          'creg01Tin" value="',
                                                                                          '"/>')
        completeRegisterData['individualResidentialAddr.creg26AddressUid'] = _GloableKeywords.subString(processResp.text,
                                                                                          'individualResidentialAddr.creg26AddressUid" value="',
                                                                                          '"/>')
        completeRegisterData['creg01Tin'] = _GloableKeywords.subString(processResp.text,
                                                                                          'creg01Tin" value="',
                                                                                          '"/>')
        completeRegisterData['creg01TaxpayerUid'] = _GloableKeywords.subString(processResp.text,
                                                                                          'creg01TaxpayerUid" value="',
                                                                                          '"/>')
        completeRegisterData['creg01PostAddrUid'] = _GloableKeywords.subString(processResp.text,
                                                                                          'creg01PostAddrUid" value="',
                                                                                          '"/>')
        completeRegisterData['creg01PhysicalAddrUid" value="'] = _GloableKeywords.subString(processResp.text,
                                                                                          'creg01PhysicalAddrUid" value="',
                                                                                          '"/>')


        '''taxtype data'''

        path = '/ITAS/reg/taxtype/config.do'
        query = 'taxpayerCategory=IND&taxpayerType=INDSP&requestUid='+completeUid+'&branchUid=&requestStatus=APPROVED&requestType=TXP_REG'
        configTaxTypeUrl=_globalVariables.BASEURL+path+'?'+query
        configTaxTypeData={'axgrid_listcols':'cret09TaxTypeName,registeredTaxType.creg06EffectiveDate,registeredTaxType.creg06Fin,registeredTaxType.creg06Status,registeredTaxType.taxpayer.creg06IsRegular,registeredTaxType.creg06ExpiryDate,registeredTaxType.taxpayer.functions',
                           'axgridid':'taxtypeview',
                           'taxtypeview_pageSize':10,
                           'taxtypeview_sort':'',
                           'taxtypeview_startIndex':0}
        configTaxTypeResp = _globalVariables.SESSION.post(configTaxTypeUrl, configTaxTypeData)

        logger.debug('configTaxTypeResp.text'+configTaxTypeResp.text)

        convertResult=_GloableKeywords.parseRespToDictOrCuple(configTaxTypeResp.text)
        completeRegisterData['registeredTaxType[0].cret09TaxtypeUid']= convertResult['cret09TaxtypeUid']
        completeRegisterData['registeredTaxType[0].creg06EffectiveDate']= convertResult['registeredTaxType']['creg06EffectiveDate']
        completeRegisterData['registeredTaxType[0].creg06RegistTaxtypeUid']= convertResult['registeredTaxType']['creg06RegistTaxtypeUid']
        completeRegisterData['registeredTaxType[0].creg06Fin']= convertResult['registeredTaxType']['creg06Fin']


        '''attachment data'''

        path = '/ITAS/reg/attachment/list.do'
        query = 'entityId='+completeUid+'&attachmentTable=TREG05_ATTACHMENT&requestUid='+completeUid+\
                '&requestStatus=APPROVED&requestType=TXP_REG&taxpayerCategory=TAXPAYER_TYPE,ID_TYPE,TAX_TYPE'
        attachmentTaxTypeUrl=_globalVariables.BASEURL+path+'?'+query
        attachmentTypeData={'attachmentview_pageSize':10,
                           'attachmentview_sort':'',
                           'attachmentview_startIndex':0,
                           'axgrid_listcols':'ccmn00DocumentTypecode,ccmn00IsUpload,ccmn00UploadDate,ccmn00Note,ccmn00ArchivedDate',
                           'axgridid':'attachmentview'}
        attachmentTypeResp = _globalVariables.SESSION.post(attachmentTaxTypeUrl, attachmentTypeData)

        attachmentResult=_GloableKeywords.parseRespToDictOrCuple(attachmentTypeResp.text)
        for i in range(3):
            completeRegisterData['attachments['+str(i)+'].ccmn00IsUpload']=attachmentResult[i]['ccmn00IsUpload']
            completeRegisterData['attachments['+str(i)+'].ccmn00Barcode']=attachmentResult[i]['ccmn00Barcode']
            completeRegisterData['attachments['+str(i)+'].ccmn00AttachUid']=attachmentResult[i]['ccmn00AttachUid']
            completeRegisterData['attachments['+str(i)+'].ccmn00DocumentTypecode']=attachmentResult[i]['ccmn00DocumentTypecode']
            completeRegisterData['attachments['+str(i)+'].ccmn00Entity']=attachmentResult[i]['ccmn00Entity']
            completeRegisterData['attachments['+str(i)+'].mandatory'] = attachmentResult[i]['mandatory']
            completeRegisterData['attachments['+str(i)+'].ccmn00IsConf'] = attachmentResult[i]['ccmn00IsConf']
            completeRegisterData['attachments['+str(i)+'].ccmn00UploadDate'] = attachmentResult[i]['ccmn00UploadDate']
            completeRegisterData['attachments['+str(i)+'].ccmn00ArchivedDate'] = attachmentResult[i]['ccmn00ArchivedDate']


        '''account data'''

        path = '/ITAS/reg/account/list.do'
        query = 'taxpayerUid=&requestStatus=APPROVED&requestType=TXP_REG&requestUid='+completeUid
        accountUrl=_globalVariables.BASEURL+path+'?'+query
        accountData={'accountview_pageSize':10,
                     'accountview_sort':'',
                     'accountview_startIndex':0,
                    'axgrid_listcols':'creg04BankName,creg04BranchName,creg04BranchNo,creg04AccountType,creg04AccountNo,creg04Holder,creg04IsShared',
                    'axgridid':'accountview'}
        accountResp = _globalVariables.SESSION.post(accountUrl, accountData)

        accountResult = _GloableKeywords.parseRespToDictOrCuple(accountResp.text)
        completeRegisterData['accounts[0].creg04AccountNo'] = accountResult['creg04AccountNo']
        completeRegisterData['accounts[0].creg04Holder'] = accountResult['creg04Holder']
        completeRegisterData['accounts[0].creg04BankName'] = accountResult['creg04BankName']
        completeRegisterData['accounts[0].creg04AccountType'] = accountResult['creg04AccountType']
        completeRegisterData['accounts[0].creg04BranchName'] = accountResult['creg04BranchName']
        completeRegisterData['accounts[0].creg04BranchNo'] = accountResult['creg04BranchNo']
        completeRegisterData['oldFirstName'] = accountResult['creg04Holder']
        completeRegisterData['parameter.account_holder_name'] = accountResult['creg04Holder']
        completeRegisterData['treg00NaturalPerson.creg00FirstName'] = accountResult['creg04Holder']
        completeRegisterData['treg00NaturalPerson.creg00Email'] = accountResult['creg04Holder']+'@qq.com'
        completeRegisterData['accounts[0].creg04AccountUid'] = accountResult['creg04AccountUid']

        '''deal with lastname'''

        completeRegisterData['oldLastName'] = searchDict['creg08Applicant'].split(accountResult['creg04Holder'])[1][1:]
        completeRegisterData['treg00NaturalPerson.creg00LastName'] = searchDict['creg08Applicant'].split(accountResult['creg04Holder'])[1][1:]

        '''submit.do'''

        path = '/ITAS/UserFlow/submit.do'
        query = 'axBizIsNew=false&axBizIsFlow=true&axBizFlowAction=complete&axBizTaskId='+axBizTaskId+ \
                '&axBizEntityType=com.cacss.itas.reg.entity.Taxpayer'
        completeUrl=_globalVariables.BASEURL+path+'?'+query
        completeResp = _globalVariables.SESSION.post(completeUrl, completeRegisterData)

        return completeResp.text

    def isCompleteRegisterSuccess(self,completeRegisterResp):
        '''check if approve register successfully
        :return true|false'''

        if 'true' in completeRegisterResp:
            logger.info('complet register successfully:'+completeRegisterResp,also_console=True)
            return True
        else:
            logger.error('complet register failed:'+completeRegisterResp)
            return False

    def getTinByRegistrationNumber(self,registrationNumber):
        '''
        get tin by registration Number
        :param registrationNumber:
        :return: tin number
        '''

        path = '/ITAS/reg/taxpayer/listData.do'
        listDataUrl=_globalVariables.BASEURL+path
        listData={
            'axgrid_listcols':'creg01Tin,creg01TaxpayerCategory,creg01TaxpayerType,taxpayerName,\
                              creg01SubmitSrc,creg01OfficeName,creg01Status,idNumber',
            'axgridid':'axgridid',
            'creg01Status':'',
            'creg01TaxpayerCategory':'IND',
            'creg01TaxpayerType':'',
            'creg01Tin':'',
            'gridview_pageSize':10,
            'gridview_sort':'',
            'gridview_startIndex':0,
            'taxpayerName':'',
            'treg00NaturalPerson.creg00IdNo':registrationNumber
        }
        listDataResp = _globalVariables.SESSION.post(listDataUrl,listData)
        listDataResult=_GloableKeywords.parseRespToDictOrCuple(listDataResp.text)
        print listDataResult
        return listDataResult['creg01Tin']