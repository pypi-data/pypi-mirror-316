
from pazer_dataform_python import ResponseForm, DataForm

vms = ResponseForm()
vms.timer = True
vms.status = True
print(vms.toResponseJSON().body)


vm = DataForm()
vm.data.rows = 0
vm.data.fetch()
print(vm.__dict__)