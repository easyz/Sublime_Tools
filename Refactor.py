import sublime, sublime_plugin
import sys
import os.path 


# class LuaRefactorFileCommand(sublime_plugin.WindowCommand):
# 	def run(self, dirs):
# 		print("_____")

        # self.window.run_command("hide_panel")
        # title = "untitle"
        # on_done = functools.partial(self.on_done, dirs[0])
        # v = self.window.show_input_panel(
        #     "File Name:", title + ".lua", on_done, None, None)
        # v.sel().clear()
        # v.sel().add(sublime.Region(0, len(title)))

		

class LuaRefactorCommand(sublime_plugin.TextCommand):

	def run(self, edit , cmd , arg):

		# 变量格式化字符串
		def FormatString():

			emptySel = None
			list = []

			for sel in self.view.sel() :

				field = self.view.substr(sel)

				if not field.strip():
					emptySel = sel
				else:
					list.append(field)


			if len(list) < 1 :
				return
			
			result = ""
			fresult = ""

			index = 0
			for s in list:
				if arg == "Lua":
					result = result + s.replace("\"","'") + " = %s \\n"
					fresult = fresult + s + ","
				elif arg == "C#":
					result = result + s.replace("\"","'") + " = {" + str(index) + "} \\n"
					fresult = fresult + s + ".ToString(),"
				index = index + 1
			
			if arg == "Lua":
				result = "print(string.format(\""+ result[:-3] +"\","+fresult[:-1]+"))"
			elif arg == "C#":
				result = "Debug.Log(string.Format(\""+ result[:-3] +"\","+fresult[:-1]+"));"

			if emptySel == None :
				sublime.set_clipboard(result)
			else:
				self.view.insert(edit,emptySel.a,result)



		# 插入打印信息
		def InsertDebugInfo():
			for sel in self.view.sel() :
				p,f = os.path.split(self.view.file_name())
				result = "\"(%s:%d)\""%(f,self.view.rowcol(sel.a)[0] + 1)
				if arg == "Lua":
					self.view.insert(edit,sel.a,"_Log("+result+")")
				elif arg == "C#":
					self.view.insert(edit,sel.a,"UnityEngine.Debug.Log("+result+");")
				




		# 空格转下划线，首字母转大写
		def ConverStringUpper():
			def Start(text):
				arg = text.split(' ')
				strp = "_"
				list = []
				for i in range(0, len(arg)):
					list.append(arg[i].capitalize())

				return strp.join(list)

			for sel in self.view.sel() :
				self.view.replace(edit,sel,Start(self.view.substr(sel)))



		# 打开文件
		def OpenFile():

			output = []
			filePath = []

			def open(index):
				if index < 0 :
					return
				self.view.window().open_file(filePath[index])

			path = sublime.get_clipboard()
			if not path.strip():
				return

			if os.path.isfile(path):
				filePath.append(path)
				open(0)
			elif os.path.isdir(path):
				listDir = os.listdir(path)
				for f in listDir:
					if os.path.isfile(path + "/"+f):
						output.append(f)
						filePath.append(path + "/"+f)

				self.view.window().show_quick_panel(output,open)



		if cmd == "format_string":
			FormatString()
		elif cmd == "insert_debug_info":
			InsertDebugInfo()
		elif cmd == "conver_string_upper":
			ConverStringUpper()
		elif cmd == "open_file":
			OpenFile()
		else:
			print("not found cmd")

