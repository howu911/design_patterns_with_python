# https://www.cnblogs.com/baxianhua/p/11141861.html

#经理类
class Manager:
     
    successor=None
    name=''
 
    def __init__(self,name):
        self.name=name
 
    #设置上级 
    def setSuccessor(self,successor):
        self.successor=successor
         
    #处理请求
    def handleRequest(self,request):
        pass
     
 
#直属经理
class LineManager(Manager):
    def handleRequest(self,request):
        if request.requestType=='little' :
            print('requestType: %s ,requestContent: %s,' %(request.requestType,request.requestContent))
            print('小事一桩，我这个小小的line manager就能搞定')
        else:
            if self.successor !=None:
                print('requestType: %s ,requestContent: %s' %(request.requestType,request.requestContent))
                print('非小事，我这个小小的line manager无能为力，交上级处理')
                print('上级是:',self.successor)
                self.successor.handleRequest(request)
 
#部门经理
class DepartmentManager(Manager):
    def handleRequest(self,request):
        if request.requestType=='middle' :
            print('requestType: %s ,requestContent: %s ' %(request.requestType,request.requestContent))
            print('中级事件，我这个department manager就能搞定')
        else:
            if  self.successor !=None:               
                print('requestType: %s ,requestContent: %s' %(request.requestType,request.requestContent))
                print('非中级事件，我这个department manager无能为力，交上级处理' )
                print('上级是:',self.successor)
                self.successor.handleRequest(request)
 
    def __str__(self):
        return 'Department Manager '
 
#总经理
class GeneralManager(Manager):
    def handleRequest(self,request):
        if request.requestType=='big' :
            print('requestType: %s ,requestContent: %s' %(request.requestType,request.requestContent))
            print('大事件，得由我这个 general manager拍板')
 
    def __str__(self):
        return 'General Manager '
 
class Request():
    def __init__(self,requestType,requestContent):
        self.requestType=requestType
        self.requestContent=requestContent
 
    def commit(self,manager):
        ret=manager.handleRequest(self)
 
 
if __name__=='__main__':
    line_manager=LineManager('Line Manager')
    department_manager=DepartmentManager('Department Manager')
    general_manager=GeneralManager('General Manager')
    line_manager.setSuccessor(department_manager)
    department_manager.setSuccessor(general_manager)
 
    print('==========================================================')
    request=Request('little','请批准团队外出腐败经费1000元')
    request.commit(line_manager)
 
    print('==========================================================')
    request=Request('middle','请批准团队外出旅游10000元')
    request.commit(line_manager)
 
    print('==========================================================')
    request=Request('big','请批准团队设备购买100000元')
    request.commit(line_manager)

