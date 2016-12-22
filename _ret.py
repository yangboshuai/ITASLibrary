import random
import time
from robot.api import logger

from APEXLibrary._global import _GloableKeywords,_globalVariables
from _itasTestData import returnData


class _RETKeywords(object):
    '''ITAS RET library'''

    def __init__(self):
        '''init function'''
        pass

    def searchTin(self,tin):
        '''search return by tin id
        _httpMethod: Post
        :return tuple (the tin's all returns)'''

        path = '/ITAS/Tret02Return/returnList/listdata.do'
        searchTinUrl = _globalVariables.BASEURL + path

        '''get tin information'''
        path='/ITAS/cmn/taxpayer/business/template.do'
        query = 'r='+str(random.random())+'&creg01Tin='+tin+'&invalidStatus=PEND_SUSP,SUSP,PEND_DEREG,DEREG,PEND_TRNS,TRNS,DEREG,PENDDER'
        templateUrl = _globalVariables.BASEURL + path + '?' + query
        templateResp=_globalVariables.SESSION.get(templateUrl)

        templateResult=_GloableKeywords.parseRespToDictOrCuple(templateResp.text)
        searchTinData={
                'axgridid': 'gridview',
                'gridview_startIndex': '0',
                'gridview_pageSize': '10',
                'gridview_sort': '',
                'creg01Tin': templateResult['creg01Tin'],
                'creg06Fin': templateResult['creg06Fin'],
                'cret09TaxTypeCode': templateResult['cret09TaxTypeCode'],
                'creg01TaxpayerUid': templateResult['creg01TaxpayerUid'],
                'creg20BranchUid': templateResult['creg20BranchUid'],
                'creg01TaxpayerCategory': templateResult['creg01TaxpayerCategory'],
                'creg01TaxpayerType': templateResult['creg01TaxpayerType'],
                'cret09TaxTypeUid': templateResult['cret09TaxTypeUid'],
                'creg01OfficeId': templateResult['creg01OfficeId'],
                'creg01Status': templateResult['creg01Status'],
                'creg00Sex': templateResult['creg00Sex'],
                'creg20BranchCode': templateResult['creg20BranchCode'],
                'creg20BranchName': templateResult['creg20BranchName'],
                'creg20IsEnabled': templateResult['creg20IsEnabled'],
                'creg01IsProvisional': templateResult['creg01IsProvisional'],
                'creg03Nature': templateResult['creg03Nature'],
                'creg01OfficeName': templateResult['creg01OfficeName'],
                'creg00HomeTel01':  '',
                'creg00HomeTel02': '',
                'creg00HomeTel03': '',
                'creg00HomeTel': templateResult['creg00HomeTel'],
                'creg00PersonName': templateResult['creg00PersonName'],
                'creg00BirthDate': templateResult['creg00BirthDate'],
                'creg00MobilePhone01': '',
                'creg00MobilePhone02': '',
                'MobilePhone': '',
                'creg02ArrivedNamibiaDate': templateResult['creg02ArrivedNamibiaDate'],
                'creg00IdNo': templateResult['creg00IdNo'],
                'creg03HeadOfficeTin': templateResult['creg03HeadOfficeTin'],
                'creg03TradeName': templateResult['creg03TradeName'],
                'creg03TradeNo': templateResult['creg03TradeNo'],
                'creg03CommencingDate': templateResult['creg03CommencingDate'],
                'cret02Barcode': '',
                'cret02RetTaxyear': '',
                'cret02RetUid': '',
                'cret03VerStatus': '',
                'axgrid_listcols': 'cret02RetUid,cret03VerNo,cret09TaxtypeCode,cret11ReturntypeCode,creg01TaxpayerUid,'
                                   'creg01Tin,cret09TaxTypeName,cret11ReturnTypeName,cret02RetTaxyear,cret02RetTaxperiod,'
                                   'cret02Periodfrom,cret02Periodto,cret02RetDuedate,cret03VerUid,cret03VerStatus'
            }

        searchTinResp=_globalVariables.SESSION.post(searchTinUrl,searchTinData)
        searchTinResult=_GloableKeywords.parseRespToDictOrCuple(searchTinResp.text)

        return searchTinResult

    def getTaxYearReturn(self,searchReturnResult,year):
        ''':param year
        :return return informatin'''

        for item in searchReturnResult:
            if str(item['cret02RetTaxyear'])==year:
                return item

    def captureReturn(self,returnInfo):
        '''capture Return keywords'''

        path='/ITAS/Tret02Return/returnList/checkCaptureRule.do'
        checkCaptureRuleUrl = _globalVariables.BASEURL + path
        checkCaptureRuleData={
            'cret11ReturntypeCode':returnInfo['cret11ReturntypeCode'],
            'cret09TaxTypeCode':returnInfo['cret09TaxtypeCode'],
            'cret03VerUid':'',
            'cret02RetTaxyear':returnInfo['cret02RetTaxyear'],
            'cret02RetTaxperiod':returnInfo['cret02RetTaxperiod'],
            'cret02Periodto':returnInfo['cret02Periodto'],
            'cret02Periodfrom':returnInfo['cret02Periodfrom'],
            'creg01TaxpayerUid':returnInfo['creg01TaxpayerUid']
        }
        checkCaptureRuleResp=_globalVariables.SESSION.post(checkCaptureRuleUrl,checkCaptureRuleData)
        if (eval(checkCaptureRuleResp.text))['success']==1:
            logger.info('the return has been captured',also_console=True)
            return
        foUid=(eval(checkCaptureRuleResp.text))['foUid']
        print 'foUid:',foUid

        path = '/ITAS/Tret02Return/returnList/returnSubmission.do'
        query='hidRetVerUid=&hidFoUid='+str(foUid)+'&captureType=&hidActionName=new&rejectReason=&hidTaxtyoeCode='
        returnSubmissionUrl = _globalVariables.BASEURL + path+'?'+query
        returnSubmissionResp=_globalVariables.SESSION.get(returnSubmissionUrl)
        returnTypeCode = _GloableKeywords.subString(returnSubmissionResp.text,'returnTypeCode="','";')
        cret02Barcode =  _GloableKeywords.subString(returnSubmissionResp.text,"cret02Barcode' readonly value='","'  /></div")
        print 'returnTypeCode:',returnTypeCode

        path = '/ITAS/cmn/taxpayer/business/template.do'
        query='r='+str(random.random())+'&creg01Tin='+returnInfo['creg01Tin']
        print returnInfo['creg01Tin']
        templateUrl = _globalVariables.BASEURL + path + '?' + query
        templateResp=_globalVariables.SESSION.get(templateUrl)
        templateResult=_GloableKeywords.parseRespToDictOrCuple(templateResp.text)
        print 'templateResp:',templateResp.text

        path = '/ITAS/reg/attachment/config.do'
        configData={'type':returnTypeCode}
        configUrl = _globalVariables.BASEURL + path
        configResp=_globalVariables.SESSION.post(configUrl,configData)
        configResult=_GloableKeywords.parseRespToDictOrCuple(configResp.text)

        print 'configResp:',configResp.text


        path = '/ITAS/Tret02Return/returnList/checkReturn.do'
        checkReturngData = {'cret11ReturntypeCode': returnInfo['cret11ReturntypeCode'],
                      'cret09TaxTypeCode': returnInfo['cret09TaxtypeCode'],
                      'cret02RetTaxyear':returnInfo['cret02RetTaxyear'],
                      'cret02RetTaxperiod':returnInfo['cret02RetTaxperiod'],
                      'creg01Tin':returnInfo['creg01Tin'],
                      'creg01TaxpayerUid':returnInfo['creg01TaxpayerUid'],
                      }
        checkReturnUrl = _globalVariables.BASEURL + path
        checkReturnResp = _globalVariables.SESSION.post(checkReturnUrl, checkReturngData)


        path = '/ITAS/Tret02Return/returnList/insert.do'
        insertData = {}
        for i in range(len(configResult)):
            insertData['attachments['+str(i)+'].modify']=''
            insertData['attachments['+str(i)+'].mandatory']='N'
            insertData['attachments['+str(i)+'].ccmn00UploadDate']=configResult[i]['systemDate']
            insertData['attachments['+str(i)+'].ccmn00Note']=''
            insertData['attachments['+str(i)+'].ccmn00IsUpload']='Y'
            insertData['attachments['+str(i)+'].ccmn00IsConf'] = 'Y'
            insertData['attachments['+str(i)+'].ccmn00Entity'] = configResult[i]['ccmn01Category']
            insertData['attachments['+str(i)+'].ccmn00DocumentTypecode'] = configResult[i]['ccmn01DocumentCode']
            insertData['attachments['+str(i)+'].ccmn00Barcode'] = ''
            insertData['attachments['+str(i)+'].ccmn00AttachUid'] = ''
            insertData['attachments['+str(i)+'].ccmn00AttachUid'] = ''
        insertData['reason']=''
        insertData['cret11ReturntypeName']=returnInfo['cret11ReturnTypeName']
        insertData['cret11ReturntypeCode'] = returnInfo['cret11ReturntypeCode']
        insertData['cret09TaxTypeUid'] = '' if returnInfo['cret11ReturntypeCode']=='null' else returnInfo['cret11ReturntypeCode']
        print 'cret09TaxTypeUid:',insertData['cret09TaxTypeUid']
        insertData['cret09TaxTypeCode'] =templateResult['cret09TaxTypeCode']
        insertData['cret02Submitsource'] ='TP'
        insertData['cret02RetUid'] ='' if returnInfo['cret02RetUid']=='null' else returnInfo['cret02RetUid']
        insertData['cret02RetTaxyear'] = returnInfo['cret02RetTaxyear']
        insertData['cret02RetTaxperiod'] = returnInfo['cret02RetTaxperiod']
        insertData['cret02RetReceivedate'] = time.strftime('%d-%m-%Y',time.localtime(time.time()))
        insertData['cret02RetDuedate'] = returnInfo['cret02RetDuedate']
        insertData['cret02Periodto'] = returnInfo['cret02Periodto']
        insertData['cret02Periodfrom'] = returnInfo['cret02Periodfrom']
        insertData['cret02Barcode'] = cret02Barcode
        insertData['cret01FoUid'] = foUid
        insertData['creg20IsEnabled'] = templateResult['creg20IsEnabled']
        insertData['creg20BranchUid'] = templateResult['creg20BranchUid']
        insertData['creg20BranchName'] = templateResult['creg20BranchName']
        insertData['creg20BranchCode'] = templateResult['creg20BranchCode']
        insertData['creg06Fin'] = templateResult['creg06Fin']
        insertData['creg03TradeNo'] = '' if templateResult['creg03TradeNo']=='null' else templateResult['creg03TradeNo']
        insertData['creg03TradeName'] = templateResult['creg03TradeName']
        insertData['creg03Nature'] = '' if templateResult['creg03Nature']=='null' else templateResult['creg03Nature']
        insertData['creg03MagisterialDistrictName'] = '' if templateResult['creg03MagisterialDistrictName']=='null' else templateResult['creg03MagisterialDistrictName']
        insertData['creg03HeadOfficeTin'] = '' if templateResult['creg03HeadOfficeTin']=='null' else templateResult['creg03HeadOfficeTin']
        insertData['creg03CommencingDate'] = '' if templateResult['creg03CommencingDate']=='null' else templateResult['creg03CommencingDate']
        insertData['creg02IsResidentName'] = templateResult['creg02IsResidentName']
        insertData['creg02ArrivedNamibiaDate'] = '' if templateResult['creg02ArrivedNamibiaDate']=='null' else templateResult['creg02ArrivedNamibiaDate']
        insertData['creg01Tin'] = returnInfo['creg01Tin']
        insertData['creg01TaxpayerUid'] = returnInfo['creg01TaxpayerUid']
        insertData['creg01TaxpayerTypeName'] = templateResult['creg01TaxpayerTypeName']
        insertData['creg01TaxpayerType'] = templateResult['creg01TaxpayerType']
        insertData['creg01TaxpayerSizeName'] = '' if templateResult['creg01TaxpayerSizeName'] == 'null' else templateResult['creg01TaxpayerSizeName']
        insertData['creg01TaxpayerName'] = templateResult['creg01TaxpayerName']
        insertData['creg01TaxpayerCategoryName'] = templateResult['creg01TaxpayerCategoryName']
        insertData['creg01TaxpayerCategory'] = templateResult['creg01TaxpayerCategory']
        insertData['creg01StatusName'] = templateResult['creg01StatusName']
        insertData['creg01Status'] = templateResult['creg01Status']
        insertData['creg01OfficeName'] = templateResult['creg01OfficeName']
        insertData['creg01OfficeId'] = templateResult['creg01OfficeId']
        insertData['creg01IsProvisional'] = templateResult['creg01IsProvisional']
        insertData['creg01EndOfFinancialMonth'] = '' if templateResult['creg01EndOfFinancialMonth'] == 'null' else templateResult['creg01EndOfFinancialMonth']
        insertData['creg01EndOfFinancialDay'] = '' if templateResult['creg01EndOfFinancialDay'] == 'null' else templateResult['creg01EndOfFinancialDay']
        insertData['creg00SexName'] = templateResult['creg00SexName']
        insertData['creg00Sex'] = templateResult['creg00Sex']
        insertData['creg00PersonName'] = templateResult['creg00PersonName']
        insertData['creg00MobilePhone'] =  '' if templateResult['creg00MobilePhone'] == 'null' else templateResult['creg00MobilePhone']
        insertData['creg00MaritalStatusName'] = templateResult['creg00MaritalStatusName']
        insertData['creg00IdNo'] = templateResult['creg00IdNo']
        insertData['creg00HomeTel'] =  '' if templateResult['creg00HomeTel'] == 'null' else templateResult['creg00HomeTel']
        insertData['creg00CitizenshipName'] = templateResult['creg00CitizenshipName']
        insertData['creg00BirthDate'] = templateResult['creg00BirthDate']
        insertData['btnSubmit'] = ''

        insertUrl = _globalVariables.BASEURL + path
        insertResp = _globalVariables.SESSION.post(insertUrl, insertData)
        return insertResp.text

    def isCaptureReturnSuccess(self,captureReturnResp):
        if 'true' in captureReturnResp:
            logger.info('capture return succuessfully:'+captureReturnResp,also_console=True)
            return True
        else:
            logger.error('capture return failed:'+captureReturnResp)
            return False

    def getReturnID(self,tin,year):
        '''
        get returnID by tin and year
        :param tin:
        :param year:
        :return: returnID
        '''


        path = '/ITAS/Tret02Return/returnList/listdata.do'
        searchTinUrl = _globalVariables.BASEURL + path

        '''get tin information'''
        path='/ITAS/cmn/taxpayer/business/template.do'
        query = 'r='+str(random.random())+'&creg01Tin='+tin+'&invalidStatus=PEND_SUSP,SUSP,PEND_DEREG,DEREG,PEND_TRNS,TRNS,DEREG,PENDDER'
        templateUrl = _globalVariables.BASEURL + path + '?' + query
        templateResp=_globalVariables.SESSION.get(templateUrl)

        templateResult=_GloableKeywords.parseRespToDictOrCuple(templateResp.text)
        searchTinData={
                'axgridid': 'gridview',
                'gridview_startIndex': '0',
                'gridview_pageSize': '10',
                'gridview_sort': '',
                'creg01Tin': templateResult['creg01Tin'],
                'creg06Fin': templateResult['creg06Fin'],
                'cret09TaxTypeCode': templateResult['cret09TaxTypeCode'],
                'creg01TaxpayerUid': templateResult['creg01TaxpayerUid'],
                'creg20BranchUid': templateResult['creg20BranchUid'],
                'creg01TaxpayerCategory': templateResult['creg01TaxpayerCategory'],
                'creg01TaxpayerType': templateResult['creg01TaxpayerType'],
                'cret09TaxTypeUid': templateResult['cret09TaxTypeUid'],
                'creg01OfficeId': templateResult['creg01OfficeId'],
                'creg01Status': templateResult['creg01Status'],
                'creg00Sex': templateResult['creg00Sex'],
                'creg20BranchCode': templateResult['creg20BranchCode'],
                'creg20BranchName': templateResult['creg20BranchName'],
                'creg20IsEnabled': templateResult['creg20IsEnabled'],
                'creg01IsProvisional': templateResult['creg01IsProvisional'],
                'creg03Nature': templateResult['creg03Nature'],
                'creg01OfficeName': templateResult['creg01OfficeName'],
                'creg00HomeTel01':  '',
                'creg00HomeTel02': '',
                'creg00HomeTel03': '',
                'creg00HomeTel': templateResult['creg00HomeTel'],
                'creg00PersonName': templateResult['creg00PersonName'],
                'creg00BirthDate': templateResult['creg00BirthDate'],
                'creg00MobilePhone01': '',
                'creg00MobilePhone02': '',
                'MobilePhone': '',
                'creg02ArrivedNamibiaDate': templateResult['creg02ArrivedNamibiaDate'],
                'creg00IdNo': templateResult['creg00IdNo'],
                'creg03HeadOfficeTin': templateResult['creg03HeadOfficeTin'],
                'creg03TradeName': templateResult['creg03TradeName'],
                'creg03TradeNo': templateResult['creg03TradeNo'],
                'creg03CommencingDate': templateResult['creg03CommencingDate'],
                'cret02Barcode': '',
                'cret02RetTaxyear': year,
                'cret02RetUid': '',
                'cret03VerStatus': '',
                'axgrid_listcols': 'cret02RetUid,cret03VerNo,cret09TaxtypeCode,cret11ReturntypeCode,creg01TaxpayerUid,'
                                   'creg01Tin,cret09TaxTypeName,cret11ReturnTypeName,cret02RetTaxyear,cret02RetTaxperiod,'
                                   'cret02Periodfrom,cret02Periodto,cret02RetDuedate,cret03VerUid,cret03VerStatus'
            }

        searchTinResp=_globalVariables.SESSION.post(searchTinUrl,searchTinData)
        searchTinResult=_GloableKeywords.parseRespToDictOrCuple(searchTinResp.text)

        return searchTinResult['cret02RetUid']

    def getBatchID(self,returnID):
        '''

        :param returnID:
        :return:
        '''

        path = '/ITAS/Tret05Batch/batchList/listdata.do'
        getBatchUrl = _globalVariables.BASEURL + path
        getBatchData={
            'gridview_startIndex':0,
            'gridview_sort':'',
            'gridview_pageSize':10,
            'cret09TaxtypeCode':'',
            'cret05BatchUid':'',
            'cret05BatchStatus':'',
            'cret02RetUid':returnID,
            'corgSubmitoffice':'',
            'corgHomeoffice':'',
            'axgridid':'gridview',
            'axgrid_listcols':'cret05BatchUid,corgHomeoffice,corgSubmitoffice,cret09TaxtypeName,cret11ReturntypeName,culgFirstCapture,culgSecondCapture,cret05BatchStatus,cret05StatusDate'
        }
        getBatchResp=_globalVariables.SESSION.post(getBatchUrl,getBatchData)
        getBatchResult=_GloableKeywords.parseRespToDictOrCuple(getBatchResp.text)
        batchID=getBatchResult['cret05BatchUid']
        logger.info('batchID:'+str(batchID),also_console=True)

        return batchID

    def sendBatch(self,batchID):
        '''
        send batch withc batchID
        :param batchID
        :return:checkNumberResp
        '''

        path = '/ITAS/Tret05Batch/batchList/detailSendBatchData.do'
        detailBatchUrl = _globalVariables.BASEURL + path
        detailBatchData={
            'foUid':batchID,
            'rnd':random.random()
        }
        detailBatchResp=_globalVariables.SESSION.post(detailBatchUrl,detailBatchData)
        returnCount=_GloableKeywords.subString(detailBatchResp.text,'rowcount:',',rows')

        path = '/ITAS/stl/report/preview.do'
        query='name=ITAS/RET/BatchCoverSheet&stlTemplateName=ITAS/RET/BatchCoverSheet&TIN=&taxpayerName=' \
              '&letterType=&issueDate=&generateOfficer=&otherParam=&batchId='+str(batchID)+'&taxpayerUID=&letterCategory='
        previewUrl = _globalVariables.BASEURL + path+'?'+query

        previewResp=_globalVariables.SESSION.post(previewUrl)

        '''_globalVariables.SESSION.get(previewResp.text)'''


        path = '/ITAS/Tret05Batch/batchList/sendBatchScreen.do'
        sendBatchUrl = _globalVariables.BASEURL + path
        sendBatchData={
            'hidId':batchID,
            'flag':'T'
        }
        sendBatchResp=_globalVariables.SESSION.post(sendBatchUrl,sendBatchData)

        path = '/ITAS/Tret05Batch/batchList/checkNumber.do'
        checkNumberUrl = _globalVariables.BASEURL + path
        checkNumberData = {
            'numberInfo':returnCount,
            'batchId': batchID
        }
        checkNumberResp = _globalVariables.SESSION.post(checkNumberUrl, checkNumberData)
        return checkNumberResp.text

    def isSendBatchSuccess(self,sendBatchRsp):
        '''
        is send batch success
        :param sendBatchRsp:
        :return: True | False
        '''
        if 'true' in sendBatchRsp:
            logger.info('send batch succuessfully:'+sendBatchRsp,also_console=True)
            return True
        else:
            logger.error('send batch failed:'+sendBatchRsp)
            return False

    def receiveBatch(self,batchID):
        '''
        receiveBatch by batchID
        :param batchID:
        :return:receiveBatchResp
        '''
        path = '/ITAS/Tret05Batch/batchList/detailBatchData.do'
        detailBatchUrl = _globalVariables.BASEURL + path
        detailBatchData={
            'foUid':batchID,
            'rnd':random.random()
        }
        detailBatchResp=_globalVariables.SESSION.post(detailBatchUrl,detailBatchData)
        returnCount=_GloableKeywords.subString(detailBatchResp.text,'rowcount:',',rows')
        print 'returnCount',returnCount


        path = '/ITAS/Tret05Batch/batchList/checkReceiveNumber.do'
        checkReceiveNumberUrl = _globalVariables.BASEURL + path
        checkReceiveNumberData = {
            'receiveNumberInfo':returnCount,
            'batchId': batchID
        }
        checkReceiveNumberResp = _globalVariables.SESSION.post(checkReceiveNumberUrl, checkReceiveNumberData)
        return checkReceiveNumberResp.text

    def isReceiveBatchSuccess(self, receiveBatchRsp):
        '''
        is send batch success
        :param sendBatchRsp:
        :return: True | False
        '''
        if 'true' in receiveBatchRsp:
            logger.info('recieve batch succuessfully:' + receiveBatchRsp, also_console=True)
            return True
        else:
            logger.error('recieve batch failed:' + receiveBatchRsp)
            return False

    def allocateBatch(self,batchID,firstCapture,secondCapture):
        '''
        allocateBatch by batchID
        :param batchID,firstCapture,secondCapture
        :return: allocateBatchResponse
        '''

        path='/ITAS/Tret05Batch/batchList/allocateBatchScreen.do'
        query='hidActionName=&isSecondRejected=&hidId='+str(batchID)
        allocateBatchScreenUrl = _globalVariables.BASEURL + path+'?'+query
        allocateBatchScreenResp=_globalVariables.SESSION.get(allocateBatchScreenUrl)

        firstCaptureID=_GloableKeywords.rSubString(allocateBatchScreenResp.text,'value="','" >'+firstCapture)
        secondCaptureID=_GloableKeywords.rSubString(allocateBatchScreenResp.text,'value="','" >'+secondCapture)
        cret11ReturntypeCode=_GloableKeywords.subString(allocateBatchScreenResp.text,"cret11ReturntypeCode' readonly value='","'")
        cret09TaxtypeCode=_GloableKeywords.subString(allocateBatchScreenResp.text,"cret09TaxtypeCode' readonly value='","'")
        cret05NumberOfReturns=_GloableKeywords.subString(allocateBatchScreenResp.text,"cret05NumberOfReturns' readonly value='","'")
        batchStatus=_GloableKeywords.subString(allocateBatchScreenResp.text,'var batchStatus = "','";')
        corgSubmitoffice=_GloableKeywords.subString(allocateBatchScreenResp.text,'corgSubmitoffice" emptyText="" defValue="','"')
        corgHomeoffice=_GloableKeywords.subString(allocateBatchScreenResp.text,'corgHomeoffice" emptyText="" defValue="','"')

        path='/ITAS/Tret05Batch/batchList/changeStatus.do'
        changeStatusUrl = _globalVariables.BASEURL + path
        changeStatusData={
            'sysdate':time.strftime('%d-%m-%Y',time.localtime(time.time())),
            'ReasonforReallocation':'',
            'culgSecondCapture':secondCaptureID,
            'culgFirstCapture':firstCaptureID,
            'cret11ReturntypeCode':cret11ReturntypeCode,
            'cret09TaxtypeCode':cret09TaxtypeCode,
            'cret05NumberOfReturns':cret05NumberOfReturns,
            'cret05BatchUid':batchID,
            'cret05BatchStatus':batchStatus,
            'corgSubmitoffice':corgSubmitoffice,
            'corgHomeoffice':corgHomeoffice,
            'btnAllocate':''
        }

        changeStatusResp=_globalVariables.SESSION.post(changeStatusUrl,changeStatusData)

        return changeStatusResp.text

    def isAllocateBatchSuccess(self,allocateBatchResp):
        '''
        is allocate batch success
        :param allocateBatchResp:
        :return: True|False
        '''

        if 'true' in allocateBatchResp:
            logger.info('allocate batch succuessfully:' + allocateBatchResp, also_console=True)
            return True
        else:
            logger.error('allocate batch failed:' + allocateBatchResp)
            return False

    def searchReturn(self,returnID):
        '''
        search return by returnID
        :param returnID:
        :return: searchReturn response tuple or list
        '''

        path = '/ITAS/Tret02Return/returnList/listdata.do'
        searchReturnUrl = _globalVariables.BASEURL + path
        searchReturnUrlData = {
            'axgridid': 'gridview',
            'gridview_startIndex': '0',
            'gridview_pageSize': '10',
            'gridview_sort': '',
            'creg01Tin':'',
            'creg06Fin': '',
            'cret09TaxTypeCode': '',
            'creg01TaxpayerUid': '',
            'creg20BranchUid': '',
            'creg01TaxpayerCategory': '',
            'creg01TaxpayerType': '',
            'cret09TaxTypeUid': '',
            'creg01OfficeId': '',
            'creg01Status': '',
            'creg00Sex': '',
            'creg20BranchCode': '',
            'creg20BranchName': '',
            'creg20IsEnabled':'',
            'creg01IsProvisional': '',
            'creg03Nature': '',
            'creg01OfficeName': '',
            'creg00HomeTel01': '',
            'creg00HomeTel02': '',
            'creg00HomeTel03': '',
            'creg00HomeTel': '',
            'creg00PersonName': '',
            'creg00BirthDate': '',
            'creg00MobilePhone01': '',
            'creg00MobilePhone02': '',
            'MobilePhone': '',
            'creg02ArrivedNamibiaDate':'',
            'creg00IdNo': '',
            'creg03HeadOfficeTin': '',
            'creg03TradeName': '',
            'creg03TradeNo': '',
            'creg03CommencingDate':'',
            'cret02Barcode': '',
            'cret02RetTaxyear': '',
            'cret02RetUid': returnID,
            'cret03VerStatus': '',
            'axgrid_listcols': 'cret02RetUid,cret03VerNo,cret09TaxtypeCode,cret11ReturntypeCode,creg01TaxpayerUid,'
                               'creg01Tin,cret09TaxTypeName,cret11ReturnTypeName,cret02RetTaxyear,cret02RetTaxperiod,'
                               'cret02Periodfrom,cret02Periodto,cret02RetDuedate,cret03VerUid,cret03VerStatus'
        }
        searchReturnResp=_globalVariables.SESSION.post(searchReturnUrl,searchReturnUrlData)
        searchReturnResult=_GloableKeywords.parseRespToDictOrCuple(searchReturnResp.text)

        return searchReturnResult

    def firstCapture(self,returnID):
        '''
        datainput1 keyworld
        :param returnID
        :return: dataInput response
        '''

        '''search return'''
        searchReturnResult=self.searchReturn(returnID)

        creg01Tin=searchReturnResult['creg01Tin']
        cret03VerUid=searchReturnResult['cret03VerUid']
        creg01TaxpayerUid=searchReturnResult['creg01TaxpayerUid']
        cret09TaxTypeCode=searchReturnResult['cret09TaxtypeCode']
        cret11ReturntypeCode=searchReturnResult['cret11ReturntypeCode']
        cret02RetTaxyear=searchReturnResult['cret02RetTaxyear']
        cret02RetTaxperiod=searchReturnResult['cret02RetTaxperiod']
        cret02Periodfrom=searchReturnResult['cret02Periodfrom']
        cret02Periodto=searchReturnResult['cret02Periodto']

        '''checkCaptureRule'''
        path = '/ITAS/Tret02Return/returnList/checkCaptureRule.do'
        checkCaptureRuleUrl=_globalVariables.BASEURL+path
        checkCaptureRuleData={
            'cret03VerUid':cret03VerUid,
            'creg01TaxpayerUid':creg01TaxpayerUid,
            'cret09TaxTypeCode':cret09TaxTypeCode,
            'cret11ReturntypeCode':cret11ReturntypeCode,
            'cret02RetTaxyear':cret02RetTaxyear,
            'cret02RetTaxperiod':cret02RetTaxperiod,
            'cret02Periodfrom':cret02Periodfrom,
            'cret02Periodto':cret02Periodto
        }
        checkCaptureRuleResp = _globalVariables.SESSION.post(checkCaptureRuleUrl,checkCaptureRuleData)
        captureType=_GloableKeywords.subString(checkCaptureRuleResp.text,'success":',',"userRule')

        '''displayConfirmOrNot'''
        path = '/ITAS/Tret02Return/returnList/displayConfirmOrNot.do'
        displayConfirmOrNotUrl = _globalVariables.BASEURL + path
        displayConfirmOrNotData={
            'captureTime':1,
            'cret03VerUid':cret03VerUid
        }

        '''changeIsCapture'''
        path='/ITAS/Tret05Batch/batchList/changeIsCapture.do'
        changeIsCaptureUrl = _globalVariables.BASEURL + path
        changeIsCaptureData={
            'cret02RetUid':returnID
        }
        changeIsCaptureResp=_globalVariables.SESSION.post(changeIsCaptureUrl,changeIsCaptureData)
        logger.info(changeIsCaptureResp.text,also_console=True)


        '''check process rule'''
        path = '/ITAS/Tret04ReturnContent/captureContent/checkProcessRule.do'
        query ='hidRetVerUid='+str(cret03VerUid)+'&hidTaxtyoeCode='+cret09TaxTypeCode+'&captureType='+str(captureType)+'&action=yes&rejectReason='
        checkProcessRuleUrl=_globalVariables.BASEURL+path+'?'+query
        checkProcessRuleResp = _globalVariables.SESSION.get(checkProcessRuleUrl)
        tableName=_GloableKeywords.subString(checkProcessRuleResp.text,'tableName:"','"')
        catagory=_GloableKeywords.subString(checkProcessRuleResp.text,'catagory:"','"')
        cret02PeriodMonthEnding=_GloableKeywords.subString(checkProcessRuleResp.text,"cret02PeriodMonthEnding' value='","'")
        cret02PeriodMonthName=_GloableKeywords.subString(checkProcessRuleResp.text,"cret02PeriodMonthName' readonly value='","'")
        cret02RetReceivedate=_GloableKeywords.subString(checkProcessRuleResp.text,"cret02RetReceivedate' value='","'")
        resourceFlag =_GloableKeywords.subString(checkProcessRuleResp.text,'resourceFlag" value="','"')
        Cret00ITPSPenEmployeeTin=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenEmployeeTin')
        Cret00ITPSPenRetveruid=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenRetveruid')
        Cret00ITPSPenTaxpayerUid=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenTaxpayerUid')
        Cret00ITPSPenTaxTypeCode=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenTaxTypeCode')
        Cret00ITPSTestReturnTypeCode=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSTestReturnTypeCode')
        Cret00ITPSTestSubmitDate=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSTestSubmitDate')

        '''template data'''
        path = '/ITAS/cmn/taxpayer/business/template.do'
        query ='r='+str(random.random())+'&creg01Tin='+str(creg01Tin)
        templateUrl=_globalVariables.BASEURL+path+'?'+query
        templateResp=_globalVariables.SESSION.get(templateUrl)
        templateResult=_GloableKeywords.parseRespToDictOrCuple(templateResp.text)

        returnData['creg00BirthDate'] =templateResult['creg00BirthDate']
        returnData['creg00CitizenshipName'] = templateResult['creg00CitizenshipName']
        returnData['creg00HomeTel'] = templateResult['creg00HomeTel']
        returnData['creg00IdNo'] = templateResult['creg00IdNo']
        returnData['creg00MaritalStatusName'] = templateResult['creg00MaritalStatusName']
        returnData['creg00MobilePhone'] = templateResult['creg00MobilePhone']
        returnData['creg00PersonName'] = templateResult['creg00PersonName']
        returnData['creg00Sex'] = templateResult['creg00Sex']
        returnData['creg00SexName'] = templateResult['creg00SexName']
        returnData['creg01EndOfFinancialDay'] = templateResult['creg01EndOfFinancialDay']
        returnData['creg01EndOfFinancialMonth'] = templateResult['creg01EndOfFinancialMonth']
        returnData['creg01IsProvisional'] = templateResult['creg01IsProvisional']
        returnData['creg01OfficeId'] = templateResult['creg01OfficeId']
        returnData['creg01OfficeName'] = templateResult['creg01OfficeName']
        returnData['creg01Status'] = templateResult['creg01Status']
        returnData['creg01StatusName'] = templateResult['creg01StatusName']
        returnData['creg01TaxpayerCategory'] = templateResult['creg01TaxpayerCategory']
        returnData['creg01TaxpayerCategoryName'] = templateResult['creg01TaxpayerCategoryName']
        returnData['creg01TaxpayerName'] = templateResult['creg01TaxpayerName']
        returnData['creg01TaxpayerSizeName'] = templateResult['creg01TaxpayerSizeName']
        returnData['creg01TaxpayerType'] = templateResult['creg01TaxpayerType']
        returnData['creg01TaxpayerTypeName'] = templateResult['creg01TaxpayerTypeName']
        returnData['creg01TaxpayerUid'] = templateResult['creg01TaxpayerUid']
        returnData['creg01Tin'] = templateResult['creg01Tin']
        returnData['creg02ArrivedNamibiaDate'] = templateResult['creg02ArrivedNamibiaDate']
        returnData['creg02IsResidentName'] = templateResult['creg02IsResidentName']
        returnData['creg03CommencingDate'] = templateResult['creg03CommencingDate']
        returnData['creg03HeadOfficeTin'] = templateResult['creg03HeadOfficeTin']
        returnData['creg03MagisterialDistrictName'] = templateResult['creg03MagisterialDistrictName']
        returnData['creg03Nature'] = templateResult['creg03Nature']
        returnData['creg03TradeName'] = templateResult['creg03TradeName']
        returnData['creg03TradeNo'] = templateResult['creg03TradeNo']
        returnData['creg06Fin'] = templateResult['creg06Fin']
        returnData['creg20BranchCode'] = templateResult['creg20BranchCode']
        returnData['creg20BranchName'] = templateResult['creg20BranchName']
        returnData['creg20BranchUid'] = templateResult['creg20BranchUid']
        returnData['creg20IsEnabled'] = templateResult['creg20IsEnabled']

        returnData['Cret00ITPSPenEmployeeTin']=Cret00ITPSPenEmployeeTin
        returnData['Cret00ITPSPenRetveruid']=Cret00ITPSPenRetveruid
        returnData['Cret00ITPSPenTaxpayerUid']=Cret00ITPSPenTaxpayerUid
        returnData['Cret00ITPSPenTaxTypeCode']=Cret00ITPSPenTaxTypeCode
        returnData['Cret00ITPSTestReturnTypeCode']=Cret00ITPSTestReturnTypeCode
        returnData['Cret00ITPSTestSubmitDate']=Cret00ITPSTestSubmitDate

        returnData['cret02Periodfrom'] = searchReturnResult['cret02Periodfrom']
        returnData['cret02PeriodMonthEnding'] = cret02PeriodMonthEnding
        returnData['cret02PeriodMonthName'] = cret02PeriodMonthName
        returnData['cret02Periodto'] = searchReturnResult['cret02Periodto']
        returnData['cret02RetDuedate'] = searchReturnResult['cret02RetDuedate']
        returnData['cret02RetReceivedate'] = cret02RetReceivedate
        returnData['cret02RetTaxperiod'] = searchReturnResult['cret02RetTaxperiod']
        returnData['cret02RetTaxyear'] = searchReturnResult['cret02RetTaxyear']
        returnData['cret02RetUid'] = searchReturnResult['cret02RetUid']
        returnData['cret02TransactionDate'] = searchReturnResult['cret02TransactionDate']
        returnData['cret03VerNo'] = searchReturnResult['cret03VerNo']
        returnData['cret03VerUid'] = searchReturnResult['cret03VerUid']
        returnData['cret09TaxTypeCode'] = searchReturnResult['cret09TaxtypeCode']
        returnData['cret09TaxtypeCode'] = searchReturnResult['cret09TaxtypeCode']
        returnData['cret09TaxTypeName'] = searchReturnResult['cret09TaxTypeName']
        returnData['cret09TaxTypeUid'] = templateResult['cret09TaxTypeUid']
        returnData['cret11ReturntypeCode'] = searchReturnResult['cret11ReturntypeCode']
        returnData['cret11ReturnTypeName'] = searchReturnResult['cret11ReturnTypeName']
        returnData['hidRetVerUid'] = cret03VerUid
        returnData['resourceFlag'] = resourceFlag
        returnData['taxPayerUid'] = searchReturnResult['creg01TaxpayerUid']


        '''attachment data'''
        path = '/ITAS/cmn/attachment/list.do'
        query ='type='+cret11ReturntypeCode+'&entityId='+str(cret03VerUid)+'&attachmentTable='+tableName+'&catagory='+catagory
        attachmentTaxTypeUrl=_globalVariables.BASEURL+path+'?'+query
        attachmentTypeData={'attachmentview_pageSize':10,
                           'attachmentview_sort':'',
                           'attachmentview_startIndex':0,
                           'axgrid_listcols':'ccmn00DocumentTypecode,ccmn00IsUpload,ccmn00UploadDate,ccmn00Note',
                           'axgridid':'attachmentview'}
        attachmentTypeResp = _globalVariables.SESSION.post(attachmentTaxTypeUrl, attachmentTypeData)
        attachmentResult=_GloableKeywords.parseRespToDictOrCuple(attachmentTypeResp.text)
        for i in range(len(attachmentResult)):
            returnData['attachments['+str(i)+'].ccmn00IsUpload']=attachmentResult[i]['ccmn00IsUpload']
            returnData['attachments['+str(i)+'].ccmn00Barcode']=''
            returnData['attachments['+str(i)+'].ccmn00AttachUid']=attachmentResult[i]['ccmn00AttachUid']
            returnData['attachments['+str(i)+'].ccmn00DocumentTypecode']=attachmentResult[i]['ccmn00DocumentTypecode']
            returnData['attachments['+str(i)+'].ccmn00Entity']=attachmentResult[i]['ccmn00Entity']
            returnData['attachments['+str(i)+'].mandatory'] = attachmentResult[i]['mandatory']
            returnData['attachments['+str(i)+'].ccmn00IsConf'] = attachmentResult[i]['ccmn00IsConf']
            returnData['attachments['+str(i)+'].ccmn00UploadDate'] = attachmentResult[i]['ccmn00UploadDate']

        '''islock'''
        path='/ITAS/islock.do'
        islockUrl = _globalVariables.BASEURL + path
        islockData={
            'businessId':str(cret03VerUid)+'RET'
        }
        islockResp=_globalVariables.SESSION.post(islockUrl,islockData)

        '''dellock'''
        path='/ITAS/dellock.do'
        dellockUrl = _globalVariables.BASEURL + path
        dellockData={
            'businessId':str(cret03VerUid)+'RET'
        }
        dellockResp=_globalVariables.SESSION.post(dellockUrl,dellockData)

        '''insertData'''
        path='/ITAS/Tret04ReturnContent/captureContent/insert.do'
        insertReturnUrl = _globalVariables.BASEURL + path
        insertReturnResp=_globalVariables.SESSION.post(insertReturnUrl,returnData)

        return insertReturnResp.text

    def isFirstCaptureSuccess(self,firstCaptureResp):
        '''check if firstCapture success
        :param firstCaptureResp
        :return True | False
         '''
        if 'true' in firstCaptureResp:
            logger.info('first capture succuessfully:' + firstCaptureResp, also_console=True)
            return True
        else:
            logger.error('first capture failed:' + firstCaptureResp)
            return False

    def secondCapture(self,returnID):
        '''
        dataInput_2 keyword
        :param returnID:
        :return:
        '''

        '''search return'''
        searchReturnResult=self.searchReturn(returnID)

        creg01Tin=searchReturnResult['creg01Tin']
        cret03VerUid=searchReturnResult['cret03VerUid']
        creg01TaxpayerUid=searchReturnResult['creg01TaxpayerUid']
        cret09TaxTypeCode=searchReturnResult['cret09TaxtypeCode']
        cret11ReturntypeCode=searchReturnResult['cret11ReturntypeCode']
        cret02RetTaxyear=searchReturnResult['cret02RetTaxyear']
        cret02RetTaxperiod=searchReturnResult['cret02RetTaxperiod']
        cret02Periodfrom=searchReturnResult['cret02Periodfrom']
        cret02Periodto=searchReturnResult['cret02Periodto']

        '''checkCaptureRule'''
        path = '/ITAS/Tret02Return/returnList/checkCaptureRule.do'
        checkCaptureRuleUrl=_globalVariables.BASEURL+path
        checkCaptureRuleData={
            'cret03VerUid':cret03VerUid,
            'creg01TaxpayerUid':creg01TaxpayerUid,
            'cret09TaxTypeCode':cret09TaxTypeCode,
            'cret11ReturntypeCode':cret11ReturntypeCode,
            'cret02RetTaxyear':cret02RetTaxyear,
            'cret02RetTaxperiod':cret02RetTaxperiod,
            'cret02Periodfrom':cret02Periodfrom,
            'cret02Periodto':cret02Periodto
        }
        checkCaptureRuleResp = _globalVariables.SESSION.post(checkCaptureRuleUrl,checkCaptureRuleData)
        captureType=_GloableKeywords.subString(checkCaptureRuleResp.text,'success":',',"userRule')

        '''/ITAS/Tret02Return/returnList/displayConfirmOrNot.do'''
        path = '/ITAS/Tret02Return/returnList/displayConfirmOrNot.do'
        displayConfirmOrNotUrl = _globalVariables.BASEURL + path
        displayConfirmOrNotData={
            'captureTime':2,
            'cret03VerUid':cret03VerUid
        }

        '''changeIsCapture'''
        path='/ITAS/Tret05Batch/batchList/changeIsCapture.do'
        changeIsCaptureUrl = _globalVariables.BASEURL + path
        changeIsCaptureData={
            'cret02RetUid':returnID
        }
        changeIsCaptureResp=_globalVariables.SESSION.post(changeIsCaptureUrl,changeIsCaptureData)
        logger.info(changeIsCaptureResp.text,also_console=True)

        '''check process rule'''
        path = '/ITAS/Tret04ReturnContent/captureContent/checkProcessRule.do'
        query ='hidRetVerUid='+str(cret03VerUid)+'&hidTaxtyoeCode='+cret09TaxTypeCode+'&captureType='+str(captureType)+'&action=yes&rejectReason='
        checkProcessRuleUrl=_globalVariables.BASEURL+path+'?'+query
        checkProcessRuleResp = _globalVariables.SESSION.get(checkProcessRuleUrl)

        tableName=_GloableKeywords.subString(checkProcessRuleResp.text,'tableName:"','"')
        catagory=_GloableKeywords.subString(checkProcessRuleResp.text,'catagory:"','"')
        cret02PeriodMonthEnding=_GloableKeywords.subString(checkProcessRuleResp.text,"cret02PeriodMonthEnding' value='","'")
        cret02PeriodMonthName=_GloableKeywords.subString(checkProcessRuleResp.text,"cret02PeriodMonthName' readonly value='","'")
        cret02RetReceivedate=_GloableKeywords.subString(checkProcessRuleResp.text,"cret02RetReceivedate' value='","'")
        resourceFlag =_GloableKeywords.subString(checkProcessRuleResp.text,'resourceFlag" value="','"')
        Cret00ITPSPenEmployeeTin=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenEmployeeTin')
        Cret00ITPSPenRetveruid=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenRetveruid')
        Cret00ITPSPenTaxpayerUid=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenTaxpayerUid')
        Cret00ITPSPenTaxTypeCode=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSPenTaxTypeCode')
        Cret00ITPSTestReturnTypeCode=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSTestReturnTypeCode')
        Cret00ITPSTestSubmitDate=_GloableKeywords.rSubString(checkProcessRuleResp.text,'value="','" id="Cret00ITPSTestSubmitDate')

        '''template data'''
        path = '/ITAS/cmn/taxpayer/business/template.do'
        query ='r='+str(random.random())+'&creg01Tin='+str(creg01Tin)
        templateUrl=_globalVariables.BASEURL+path+'?'+query
        templateResp=_globalVariables.SESSION.get(templateUrl)
        templateResult=_GloableKeywords.parseRespToDictOrCuple(templateResp.text)

        returnData['creg00BirthDate'] =templateResult['creg00BirthDate']
        returnData['creg00CitizenshipName'] = templateResult['creg00CitizenshipName']
        returnData['creg00HomeTel'] = templateResult['creg00HomeTel']
        returnData['creg00IdNo'] = templateResult['creg00IdNo']
        returnData['creg00MaritalStatusName'] = templateResult['creg00MaritalStatusName']
        returnData['creg00MobilePhone'] = templateResult['creg00MobilePhone']
        returnData['creg00PersonName'] = templateResult['creg00PersonName']
        returnData['creg00Sex'] = templateResult['creg00Sex']
        returnData['creg00SexName'] = templateResult['creg00SexName']
        returnData['creg01EndOfFinancialDay'] = templateResult['creg01EndOfFinancialDay']
        returnData['creg01EndOfFinancialMonth'] = templateResult['creg01EndOfFinancialMonth']
        returnData['creg01IsProvisional'] = templateResult['creg01IsProvisional']
        returnData['creg01OfficeId'] = templateResult['creg01OfficeId']
        returnData['creg01OfficeName'] = templateResult['creg01OfficeName']
        returnData['creg01Status'] = templateResult['creg01Status']
        returnData['creg01StatusName'] = templateResult['creg01StatusName']
        returnData['creg01TaxpayerCategory'] = templateResult['creg01TaxpayerCategory']
        returnData['creg01TaxpayerCategoryName'] = templateResult['creg01TaxpayerCategoryName']
        returnData['creg01TaxpayerName'] = templateResult['creg01TaxpayerName']
        returnData['creg01TaxpayerSizeName'] = templateResult['creg01TaxpayerSizeName']
        returnData['creg01TaxpayerType'] = templateResult['creg01TaxpayerType']
        returnData['creg01TaxpayerTypeName'] = templateResult['creg01TaxpayerTypeName']
        returnData['creg01TaxpayerUid'] = templateResult['creg01TaxpayerUid']
        returnData['creg01Tin'] = templateResult['creg01Tin']
        returnData['creg02ArrivedNamibiaDate'] = templateResult['creg02ArrivedNamibiaDate']
        returnData['creg02IsResidentName'] = templateResult['creg02IsResidentName']
        returnData['creg03CommencingDate'] = templateResult['creg03CommencingDate']
        returnData['creg03HeadOfficeTin'] = templateResult['creg03HeadOfficeTin']
        returnData['creg03MagisterialDistrictName'] = templateResult['creg03MagisterialDistrictName']
        returnData['creg03Nature'] = templateResult['creg03Nature']
        returnData['creg03TradeName'] = templateResult['creg03TradeName']
        returnData['creg03TradeNo'] = templateResult['creg03TradeNo']
        returnData['creg06Fin'] = templateResult['creg06Fin']
        returnData['creg20BranchCode'] = templateResult['creg20BranchCode']
        returnData['creg20BranchName'] = templateResult['creg20BranchName']
        returnData['creg20BranchUid'] = templateResult['creg20BranchUid']
        returnData['creg20IsEnabled'] = templateResult['creg20IsEnabled']

        returnData['Cret00ITPSPenEmployeeTin']=Cret00ITPSPenEmployeeTin
        returnData['Cret00ITPSPenRetveruid']=Cret00ITPSPenRetveruid
        returnData['Cret00ITPSPenTaxpayerUid']=Cret00ITPSPenTaxpayerUid
        returnData['Cret00ITPSPenTaxTypeCode']=Cret00ITPSPenTaxTypeCode
        returnData['Cret00ITPSTestReturnTypeCode']=Cret00ITPSTestReturnTypeCode
        returnData['Cret00ITPSTestSubmitDate']=Cret00ITPSTestSubmitDate

        returnData['cret02Periodfrom'] = searchReturnResult['cret02Periodfrom']
        returnData['cret02PeriodMonthEnding'] = cret02PeriodMonthEnding
        returnData['cret02PeriodMonthName'] = cret02PeriodMonthName
        returnData['cret02Periodto'] = searchReturnResult['cret02Periodto']
        returnData['cret02RetDuedate'] = searchReturnResult['cret02RetDuedate']
        returnData['cret02RetReceivedate'] = cret02RetReceivedate
        returnData['cret02RetTaxperiod'] = searchReturnResult['cret02RetTaxperiod']
        returnData['cret02RetTaxyear'] = searchReturnResult['cret02RetTaxyear']
        returnData['cret02RetUid'] = searchReturnResult['cret02RetUid']
        returnData['cret02TransactionDate'] = searchReturnResult['cret02TransactionDate']
        returnData['cret03VerNo'] = searchReturnResult['cret03VerNo']
        returnData['cret03VerUid'] = searchReturnResult['cret03VerUid']
        returnData['cret09TaxTypeCode'] = searchReturnResult['cret09TaxtypeCode']
        returnData['cret09TaxtypeCode'] = searchReturnResult['cret09TaxtypeCode']
        returnData['cret09TaxTypeName'] = searchReturnResult['cret09TaxTypeName']
        returnData['cret09TaxTypeUid'] = templateResult['cret09TaxTypeUid']
        returnData['cret11ReturntypeCode'] = searchReturnResult['cret11ReturntypeCode']
        returnData['cret11ReturnTypeName'] = searchReturnResult['cret11ReturnTypeName']
        returnData['hidRetVerUid'] = cret03VerUid
        returnData['resourceFlag'] = resourceFlag
        returnData['taxPayerUid'] = searchReturnResult['creg01TaxpayerUid']


        '''attachment data'''
        path = '/ITAS/cmn/attachment/list.do'
        query ='type='+cret11ReturntypeCode+'&entityId='+str(cret03VerUid)+'&attachmentTable='+tableName+'&catagory='+catagory
        attachmentTaxTypeUrl=_globalVariables.BASEURL+path+'?'+query
        attachmentTypeData={'attachmentview_pageSize':10,
                           'attachmentview_sort':'',
                           'attachmentview_startIndex':0,
                           'axgrid_listcols':'ccmn00DocumentTypecode,ccmn00IsUpload,ccmn00UploadDate,ccmn00Note',
                           'axgridid':'attachmentview'}
        attachmentTypeResp = _globalVariables.SESSION.post(attachmentTaxTypeUrl, attachmentTypeData)
        attachmentResult=_GloableKeywords.parseRespToDictOrCuple(attachmentTypeResp.text)
        for i in range(len(attachmentResult)):
            returnData['attachments['+str(i)+'].ccmn00IsUpload']=attachmentResult[i]['ccmn00IsUpload']
            returnData['attachments['+str(i)+'].ccmn00Barcode']=''
            returnData['attachments['+str(i)+'].ccmn00AttachUid']=attachmentResult[i]['ccmn00AttachUid']
            returnData['attachments['+str(i)+'].ccmn00DocumentTypecode']=attachmentResult[i]['ccmn00DocumentTypecode']
            returnData['attachments['+str(i)+'].ccmn00Entity']=attachmentResult[i]['ccmn00Entity']
            returnData['attachments['+str(i)+'].mandatory'] = attachmentResult[i]['mandatory']
            returnData['attachments['+str(i)+'].ccmn00IsConf'] = attachmentResult[i]['ccmn00IsConf']
            returnData['attachments['+str(i)+'].ccmn00UploadDate'] = attachmentResult[i]['ccmn00UploadDate']

        '''islock'''
        path='/ITAS/islock.do'
        islockUrl = _globalVariables.BASEURL + path
        islockData={
            'businessId':str(cret03VerUid)+'RET'
        }
        islockResp=_globalVariables.SESSION.post(islockUrl,islockData)

        '''dellock'''
        path='/ITAS/dellock.do'
        dellockUrl = _globalVariables.BASEURL + path
        dellockData={
            'businessId':str(cret03VerUid)+'RET'
        }
        dellockResp=_globalVariables.SESSION.post(dellockUrl,dellockData)

        '''secondCaptureInsert'''
        path='/ITAS/Tret04ReturnContent/captureContent/secondCaptureInsert.do'
        insertReturnUrl = _globalVariables.BASEURL + path
        insertReturnResp=_globalVariables.SESSION.post(insertReturnUrl,returnData)
        return insertReturnResp.text

    def isSecondCaptureSuccess(self, secondCaptureResp):
        '''check if secondCapture success
        :param secondCaptureResp
        :return True | False
         '''
        if 'true' in secondCaptureResp:
            logger.info('second Capture succuessfully:' + secondCaptureResp, also_console=True)
            return True
        else:
            logger.error('second Capture failed:' + secondCaptureResp)
            return False

