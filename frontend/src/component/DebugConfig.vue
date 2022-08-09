<template>
<div>
<!--  <button>{{ this.language }}</button>-->
</div>
</template>

<script>
export default {
  name: "DebugConfig",
  data(){
    return{
      language:"python"
    }
  },


  methods: {
    get_set_breakpoints_order(breakpointslist = []) {
      let order = ''
      for (let i = 0; i < breakpointslist.length; i++) {
        order = order + 'b ' + breakpointslist[i] + '\n'
      }
      return order
    },
    get_continue_order() {
      return 'c\n'
    },
    get_next_order() {
      return 'n\n'
    },
    get_step_in_order() {
      return 's\n'
    },
    get_step_out_order() {
      return 'return\n'
    },
    get_stop_order() {
      return 'quit\n'
    },
    get_line_order() {
      return 'line\n'+'{k:v for k,v in locals().items() if \'__\' not in k and \'pdb\' not in k}\n'
    },
    get_locals(){
      return '{k:v for k,v in locals().items() if \'__\' not in k and \'pdb\' not in k}\n'
    },
    handleOutput(data_output,this_pointer){
      let output=data_output
      // var lineno=1
      var last_character = data_output[data_output.length - 2]
        var tmp = data_output.lastIndexOf("\n")
        if (last_character == '$') {
          if (tmp != -1) {
            output = data_output.slice(0, data_output.lastIndexOf("\n") + 1) + "$ "
          } else {
            output = data_output.substring(data_output.length - 2)
          }
        }
        let tmp_idx_begin=data_output.lastIndexOf("[my-pdb]")


          let tmp_idx = data_output.lastIndexOf("lineno:")
          let tmp_idx_num_end = data_output.lastIndexOf(".end")
          let left_idx_locals = data_output.lastIndexOf("{")
          let right_idx_locals = data_output.lastIndexOf("}")
          if (tmp_idx !== -1 && tmp_idx_num_end !== -1) {
            try {
              let line_no = parseInt(data_output.substring(tmp_idx + 7, tmp_idx_num_end));
              this_pointer.$refs.child.changeline(line_no);
              // console.log('change line to ' + line_no)
            } catch (e) {
              console.error(e)
            }
            if (left_idx_locals !== -1 && right_idx_locals !== -1) {
              let local_variables = data_output.substring(left_idx_locals, right_idx_locals + 1);
              if(local_variables.lastIndexOf('{k:v for )')===-1) {
                this_pointer.monitoredVariables = local_variables;
              }

            }
          }
          else if (left_idx_locals !== -1 && right_idx_locals !== -1) {
              let local_variables = data_output.substring(left_idx_locals, right_idx_locals + 1);
              if(local_variables.lastIndexOf('{k:v for )')===-1) {
                this_pointer.monitoredVariables = local_variables;
              }

            }
          else {
            this_pointer.debug_console.write(output);
          }
    }
}
}
</script>


<style scoped>

</style>