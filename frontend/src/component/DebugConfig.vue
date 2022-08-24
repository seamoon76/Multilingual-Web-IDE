<template>
<div>
<!--  <button>{{ this.language }}</button>-->
</div>
</template>

<script>
//import UTF8 from "utf-8";


export default {
  name: "DebugConfig",
  data() {
    return {
      language: "python"
    }
  },


  methods: {
    get_set_breakpoints_order(breakpointslist = [], language) {
      let order = ''
      if (language === 'python') {

        for (let i = 0; i < breakpointslist.length; i++) {
          order = order + 'b ' + breakpointslist[i] + '\n'
        }

      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        for (let i = 0; i < breakpointslist.length; i++) {
          order = order + 'break ' + breakpointslist[i] + '\n'
        }
      }
      return order
    },
    start(language) {
      let order = ''
      if (language === 'c' || language === 'cpp' || language === 'c++') {
        order = order + 'start\n'
      } else if (language === 'python') {
        order = order + 'c\n'
      }

      return order
    },
    get_continue_order(language) {
      if (language === 'python') {
        return 'c\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        return 'c\n'
      }
      // you can add new language here
      //
      //
    },
    get_next_order(language) {

      if (language === 'python') {
        return 'n\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        return 'next\n'

      }
    },
    get_step_in_order(language) {

      if (language === 'python') {
        return 's\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        return 'step\n'

      }
    },
    get_step_out_order(language) {
      if (language === 'python') {
        return 'r\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        return 'finish\n'
      }
    },
    get_stop_order(language) {
      if (language === 'python') {
        return 'q\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        return 'quit\ny\n'
      }

    },
    get_line_order(language) {
      if (language === 'python') {
        return 'line\n' + '{k:v for k,v in locals().items() if \'__\' not in k and \'pdb\' not in k}\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {
        return 'where\n' + 'info locals\n'
      }

    },
    get_frame(language) {
      if (language === 'python') {
        return 'frame\n'
      }
    },
    get_locals(language) {
      if (language === 'python') {
        return '{k:v for k,v in locals().items() if \'__\' not in k and \'pdb\' not in k}\n'
      } else if (language === 'c' || language === 'cpp' || language === 'c++') {

      }

    },
    // utf8To16(input) {
    //   var _escape = function (s) {
    //     function q(c) {
    //       c = c.charCodeAt();
    //       return '%' + (c < 16 ? '0' : '') + c.toString(16).toUpperCase();
    //     }
    //
    //     return s.replace(/[\x00-),:-?[-^`{-\xFF]/g, q);
    //   };
    //   try {
    //     return decodeURIComponent(_escape(input));
    //   } catch (URIError) {
    //     //include invalid character, cannot convert
    //     return input;
    //   }
    // },
    handleOutput(data_output, this_pointer, language) {
      if (language === 'python') {
        let output = data_output
        if (output.lastIndexOf('PS1="$"') !== -1) {
          this_pointer.debug_console.write('$');
          return
        }

        if(data_output.indexOf("will be restarted")!==-1)
        {
          let info_index=data_output.indexOf("The program finished");
          let info=data_output.substring(0,info_index)
          this_pointer.debug_console.write(info)
          this_pointer.debug_console.write("\nThe program finished.\n");
          this_pointer.stopDebuging();
          return
        }
        else if (data_output.endsWith("(my-pdb)") && data_output.indexOf(".frameEnd") == -1 && data_output.indexOf(".end") == -1 && this_pointer.debugState) {
          this_pointer.debug_console.write(output);
          //console.log(133)
          this_pointer.socket.emit("pty-input", {input: this.get_frame(language)});
          //console.log(135)

        } else if (data_output.indexOf(".frameEnd") != -1 && this_pointer.debugState)//返回了frame
        {
          let tmp_idx = data_output.lastIndexOf("frame:")
          let tmp_idx_num_end = data_output.lastIndexOf(".frameEnd")

          if (tmp_idx !== -1 && tmp_idx_num_end !== -1) {
            try {
              let frameData = JSON.parse(data_output.substring(tmp_idx + 6, tmp_idx_num_end));
              let line_no = parseInt(frameData['lineno'])
              let local_variables = frameData['locals']
              let filename = frameData['filename']
              let dirpath = frameData['dirpath']
              let breaklist = frameData['breakpoints'][0]
              console.log(line_no,local_variables,filename,dirpath,breaklist)
              if (filename != this_pointer.$refs.child.filename) {
                this_pointer.$refs.child.filename = filename
                this_pointer.$refs.child.uploadCodeFullPath(dirpath, filename, line_no)
              }
              else {
                this_pointer.$refs.child.changeline(line_no);
              }
              this_pointer.monitoredVariables = local_variables.toString();
              
            } catch (e) {
              console.error(e)
            }
          }
        } else if (data_output.indexOf(".end") != -1 && this_pointer.debugState)//返回了行号
          {
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
                if (local_variables.lastIndexOf('{k:v for )') === -1) {
                  this_pointer.monitoredVariables = local_variables;
                }

              }
            } else if (left_idx_locals !== -1 && right_idx_locals !== -1) {
              let local_variables = data_output.substring(left_idx_locals, right_idx_locals + 1);
              if (local_variables.lastIndexOf('{k:v for )') === -1) {
                this_pointer.monitoredVariables = local_variables;
              }
            }
          } else if(this_pointer.debugState){
            this_pointer.debug_console.write(output);
          }
        } else if (language === 'c' || language === 'cpp' || language === 'c++') {
          let output = data_output
          // if (output.lastIndexOf('PS1="$"') === -1) {
          //   return
          // }
          if (output.lastIndexOf('PS1="$"') !== -1) {
            this_pointer.debug_console.write('$');
            return
          }
          let re = /#.*(\.c|\.cpp|\.h|\.hpp).*\d+/;
          if (data_output.search("exited") !== -1) {
            this_pointer.debugState = false;
            this_pointer.$refs.child.changeline(1);
            this_pointer.debug_console.write('$ exited');
            return
          }


          if (data_output.endsWith("(gdb) ") && data_output.search("exited normally") == -1 && data_output.search(re) == -1 && this_pointer.debugState) {
            this_pointer.debug_console.write(output);
            this_pointer.socket.emit("pty-input", {input: this.get_line_order(language)});

          } else if (data_output.endsWith("(gdb) ") && data_output.search("exited normally") == -1 && data_output.search(re) >= 0)//返回了行号和变量
          {
            let tmp_idx = data_output.search(/(\.c|\.cpp|\.h|\.hpp).*\d+/)
            let line_num = data_output.substring(tmp_idx + 2, tmp_idx + 10).replace(/[^0-9]/ig, "")
            try {
              let line_no = parseInt(line_num);
              this_pointer.$refs.child.changeline(line_no);
            } catch (e) {
              console.error(e)
            }
            let str_locals = data_output.match(/locals\s([\s\S]*)\(gdb\)/)[1]
            let split_strs=str_locals.split("\n");
            for(let i=0;i<split_strs.length;i++){

              if(split_strs[i].indexOf("__")!==-1)
              {
                //console.log(split_strs[i])
                str_locals=str_locals.replace(split_strs[i],"")
              }
            }

            if (data_output.match(/locals\s([\s\S]*)\(gdb\)/) != null) {
              // let b=utf8.encode(str_locals)
              // console.log(b)
              //let bytes_array=UTF8.setBytesFromString(str_locals);
              // let u16=this.utf8To16(str_locals)
              // console.log(u16)
              //   this_pointer.monitoredVariables = u16
              if(language=='c')
              {
                str_locals=str_locals.replace(/.\[([23]\d)?m/g, "")
              }
              else {
                str_locals = str_locals.replace(/.\[([23]\d)?m/g, "")
              }
              this_pointer.monitoredVariables = str_locals
              //console.log("monitoredVariables:",this_pointer.monitoredVariables)
            }
          } else if(output!=="where"){
            this_pointer.debug_console.write(output);
          }
        }
      }
    }

}
</script>


<style scoped>

</style>