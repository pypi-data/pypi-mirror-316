
from pazer_dataform_python import ResponseForm, DataForm

vms = ResponseForm()
vms.timer = True
vms.status = True
print(vms.toResponseJSON().body)


vm = DataForm()
vm.data.items =[]
vm.data.fetch()
print(vm.data.__dict__)