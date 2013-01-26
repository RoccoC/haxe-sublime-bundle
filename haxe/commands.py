#import haxe.complete




import sublime, sublime_plugin



from haxe.log import log




from sublime import Region

import os



import haxe.project as hxproject


import haxe.codegen

import haxe.tools.path as path_tools

#class HaxelibExecCommand(stexec.ExecCommand):
#
#	def run(self, *args, **kwargs):
#
#		print "hello running"
#		super(HaxelibExecCommand, self).run(*args, **kwargs)
#
#	def finish(self, *args, **kwargs):
#		super(HaxelibExecCommand, self).finish(*args, **kwargs)  
#		print "haxelibExec"
#		hxlib.HaxeLib.scan()

class HaxeGetTypeOfExprCommand (sublime_plugin.TextCommand ):
	def run( self , edit ) :
		

		view = self.view
		
		file_name = view.file_name()

		if file_name == None:
			return

		file_name = os.path.basename(view.file_name())

		window = view.window()
		folders = window.folders()
 
		projectDir = folders[0]
		tmp_folder = folders[0] + "/tmp"
		target_file = folders[0] + "/tmp/" + file_name

		if os.path.exists(tmp_folder):
			path_tools.remove_dir(tmp_folder)			
		

		os.makedirs(tmp_folder)
		

		fd = open(target_file, "w+")
		sel = view.sel()

		word = view.substr(sel[0])

		replacement = "(hxsublime.Utils.getTypeOfExpr(" + word + "))."

		newSel = Region(sel[0].a, sel[0].a + len(replacement))


		view.replace(edit, sel[0], replacement)

		newSel = view.sel()[0]

		view.replace(edit, newSel, word)

		new_content = view.substr(sublime.Region(0, view.size()))
		fd.write(new_content)

		view.run_command("undo")


class HaxeDisplayCompletion( sublime_plugin.TextCommand ):

	def run( self , edit ) :

		log("run HaxeDisplayCompletion")
		
		view = self.view
		project = hxproject.current_project(self.view)
		project.completion_context.set_manual_trigger(view, False)
		

		self.view.run_command( "auto_complete" , {
			"api_completions_only" : True,
			"disable_auto_insert" : True,
			"next_completion_if_showing" : False,
			'auto_complete_commit_on_tab': True
		})


class HaxeDisplayMacroCompletion( sublime_plugin.TextCommand ):
	
	def run( self , edit ) :
		
		log("run HaxeDisplayMacroCompletion")
		
		view = self.view
		project = hxproject.current_project(view)
		project.completion_context.set_manual_trigger(view, True)
		
		
		view.run_command( "auto_complete" , {
			"api_completions_only" : True,
			"disable_auto_insert" : True,
			"next_completion_if_showing" : True
		} )

		

class HaxeInsertCompletionCommand( sublime_plugin.TextCommand ):
	
	def run( self , edit ) :
		log("run HaxeInsertCompletion")
		view = self.view

		view.run_command( "insert_best_completion" , {
			"default" : ".",
			"exact" : True
		} )

class HaxeSaveAllAndBuildCommand( sublime_plugin.TextCommand ):
	def run( self , edit ) :
		log("run HaxeSaveAllAndBuildCommand")
		view = self.view
		view.window().run_command("save_all")
		hxproject.current_project(self.view).run_build( view )

class HaxeRunBuildCommand( sublime_plugin.TextCommand ):
	def run( self , edit ) :
		view = self.view
		log("run HaxeRunBuildCommand")
		hxproject.current_project(self.view).run_build( view )


class HaxeSelectBuildCommand( sublime_plugin.TextCommand ):
	def run( self , edit ) :
		log("run HaxeSelectBuildCommand")
		view = self.view
		
		hxproject.current_project(self.view).select_build( view )

# called 
class HaxeHintCommand( sublime_plugin.TextCommand ):
	def run( self , edit ) :
		log("run HaxeHintCommand")
		
		view = self.view
		
		view.run_command('auto_complete', {'disable_auto_insert': True})
		


class HaxeRestartServerCommand( sublime_plugin.WindowCommand ):

	def run( self ) : 
		log("run HaxeRestartServerCommand")
		view = sublime.active_window().active_view()
		
		project = hxproject.current_project(self.view)

		project.server.stop_server()
		project.server.start_server( view )



class HaxeGenerateUsingCommand( sublime_plugin.TextCommand ):
	def run( self , edit ) :
		log("run HaxeGenerateUsingCommand")
		haxe.codegen.generate_using(self.view, edit)
		

class HaxeGenerateImportCommand( sublime_plugin.TextCommand ):

	def run( self, edit ) :
		log("run HaxeGenerateImportCommand")
		
		haxe.codegen.generate_import(self.view, edit)
		