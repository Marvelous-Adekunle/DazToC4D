import c4d 
import os
import sys
from c4d import gui, documents

folder = os.path.dirname( __file__ )
if folder not in sys.path: 
    sys.path.insert( 0, folder )
from Utilities import dazToC4Dutils
from DazToC4DClasses import DazToC4D
from Materials import Materials, convertToRedshift, convertMaterials
from CustomIterators import ObjectIterator, TagIterator

class guiDazToC4DMain(gui.GeDialog):
    
    dialog = None
    extraDialog = None
    
    BUTTON_CONFIG = 923123
    BUTTON_AUTO_IMPORT_FIG = 923124
    BUTTON_AUTO_IMPORT_PROP = 923131
    BUTTON_CONVERT_MATERIALS = 923126
    BUTTON_CONFIG = 923127
    BUTTON_TEMP = 923128
    BUTTON_HELP = 923129
    BUTTON_AUTO_IK = 923130


    MY_BITMAP_BUTTON = 9353535

    LogoButton = ''

    dir, file = os.path.split(__file__)  # Gets the plugin's directory
    daztoC4D_Folder = os.path.join(dir, 'res')  # Adds the res folder to the path
    
    # Set Images for UI
    img_d2c4dLogo = os.path.join(daztoC4D_Folder, 'd2c4d_logo.png')
    img_loading = os.path.join(daztoC4D_Folder, 'd2c4d_loading.png')
    img_d2c4dHelp = os.path.join(daztoC4D_Folder, 'd2c4d_help.png')
    img_btnAutoImport_FIG = os.path.join(daztoC4D_Folder, 'btnGenesisImport.png')
    img_btnAutoImportOff_FIG = os.path.join(daztoC4D_Folder, 'btnGenesisImport.png')
    img_btnAutoImport_PROP = os.path.join(daztoC4D_Folder, 'btnPropImport.png')
    img_btnAutoImportOff_PROP = os.path.join(daztoC4D_Folder, 'btnPropImport.png')
    img_btnManualImport = os.path.join(daztoC4D_Folder, 'btnImport.png')
    img_btnManualImportOff = os.path.join(daztoC4D_Folder, 'btnImport0.png')
    img_btnConvertMaterials = os.path.join(daztoC4D_Folder, 'btnConvertMaterials.png')
    img_btnConvertMaterialsOff = os.path.join(daztoC4D_Folder, 'btnConvertMaterials0.png')
    img_btnAutoIK = os.path.join(daztoC4D_Folder, 'btnAutoIK.png')
    img_btnAutoIKOff = os.path.join(daztoC4D_Folder, 'btnAutoIK0.png')
    img_btnConfig = os.path.join(daztoC4D_Folder, 'btnConfig.png')


    def __init__(self):
        try:
            self.AddGadget(c4d.DIALOG_NOMENUBAR, 0)#disable menubar
        except:
            pass

    def buttonsChangeState(self, btnState):
            c4d.StatusClear()
            c4d.EventAdd()
            c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
            c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW | c4d.DRAWFLAGS_NO_THREAD  | c4d.DRAWFLAGS_STATICBREAK)
            c4d.DrawViews(c4d.EVMSG_CHANGEDSCRIPTMODE)
            c4d.EventAdd(c4d.EVENT_ANIMATE)
            c4d.StatusClear()
            if btnState == False:
                self.main_logo.SetImage(self.img_loading, False)  # Add the image to the button
                try:
                    self.main_logo.LayoutChanged()
                    self.main_logo.Redraw()
                except:
                    print("DazToC4D: LayoutChanged skip...")

                self.auto_import_fig_but.SetImage(self.img_btnAutoImportOff_FIG, False)  # Add the image to the button
                self.auto_import_prop_but.SetImage(self.img_btnAutoImportOff_PROP, False)  # Add the image to the button
                self.convert_mat_but.SetImage(self.img_btnConvertMaterialsOff, False)  # Add the image to the button
                self.auto_ik_but.SetImage(self.img_btnAutoIKOff, False)  # Add the image to the button

            if btnState == True:
                self.main_logo.SetImage(self.img_d2c4dLogo, False)  # Add the image to the button
                self.auto_import_fig_but.SetImage(self.img_btnAutoImport_FIG, False)  # Add the image to the button
                self.auto_import_prop_but.SetImage(self.img_btnAutoImport_PROP, False)  # Add the image to the button
                self.convert_mat_but.SetImage(self.img_btnConvertMaterials, False)  # Add the image to the button
                self.auto_ik_but.SetImage(self.img_btnAutoIK, False)  # Add the image to the button

            bc = c4d.BaseContainer()
            c4d.gui.GetInputState(c4d.BFM_INPUT_MOUSE, c4d.BFM_INPUT_CHANNEL, bc)

            return True

    def buttonBC(self, tooltipText="", presetLook=""):
        # Logo Image #############################################################
        bc = c4d.BaseContainer()  # Create a new container to store the button image
        bc.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        bc.SetString(c4d.BITMAPBUTTON_TOOLTIP, tooltipText)

        if presetLook == "":
            bc.SetInt32(c4d.BITMAPBUTTON_BORDER, c4d.BORDER_ROUND)  # Sets the border to look like a button
        if presetLook == "Preset0":
            bc.SetInt32(c4d.BITMAPBUTTON_BORDER, c4d.BORDER_NONE)  # Sets the border to look like a button
        if presetLook == "Preset1":
            bc.SetInt32(c4d.BITMAPBUTTON_BORDER, c4d.BORDER_NONE)  # Sets the border to look like a button
            bc.SetBool(c4d.BITMAPBUTTON_BUTTON, False)

        return bc
        # Logo Image #############################################################


    def CreateLayout(self):
        self.SetTitle('DazToC4D v1.1.2')
        self.AddSeparatorH(c4d.BFV_SCALEFIT)  # Separator H

        # Logo Image #############################################################
        bc = c4d.BaseContainer()  # Create a new container to store the button image
        bc.SetInt32(c4d.BITMAPBUTTON_BORDER, c4d.BORDER_ROUND)  # Sets the border to look like a button
        self.LogoButton = self.AddCustomGui(self.MY_BITMAP_BUTTON, c4d.CUSTOMGUI_BITMAPBUTTON, "Logo", c4d.BFH_CENTER, 0, 0, bc)
        self.LogoButton.SetImage(self.img_d2c4dLogo, False)  # Add the image to the button
    
        self.main_logo = self.LogoButton
        print('**********************')
        print(self.LogoButton)
        print('**********************')

        # Logo Image #############################################################

        # Import
        self.GroupBegin(10000, c4d.BFH_CENTER, 1, title='')
        self.GroupBorderNoTitle(c4d.BORDER_OUT)
        self.GroupBorderSpace(0, 0, 0, 0)

        self.GroupBegin(10000, c4d.BFH_SCALEFIT, 5)  # BEGIN ----------------------
        self.GroupBorderNoTitle(c4d.BORDER_NONE)
        self.GroupBorderSpace(12, 5, 10, 5)

        self.LogoButton6 = self.AddCustomGui(self.BUTTON_CONFIG, c4d.CUSTOMGUI_BITMAPBUTTON, "Bitmap Button", c4d.BFH_CENTER, 0, 0, self.buttonBC("", "Preset0"))
        self.LogoButton6.SetImage(self.img_btnConfig, True)  # Add the image to the button

        self.AddSeparatorV(0, c4d.BFV_SCALEFIT)  # Separator V

        self.GroupBegin(10000, c4d.BFH_CENTER, 1, title='')
        self.GroupBorderNoTitle(c4d.BORDER_OUT)
        self.GroupBorderSpace(0, 0, 0, 0)
        self.LogoButton6 = self.AddCustomGui(self.BUTTON_AUTO_IMPORT_FIG, c4d.CUSTOMGUI_BITMAPBUTTON, "Bitmap Button", c4d.BFH_CENTER, 0, 0, self.buttonBC("", "Preset0"))
        self.LogoButton6.SetImage(self.img_btnAutoImportOff_FIG, True)  # Add the image to the button
        self.auto_import_fig_but = self.LogoButton6

        self.LogoButton7 = self.AddCustomGui(self.BUTTON_AUTO_IMPORT_PROP, c4d.CUSTOMGUI_BITMAPBUTTON, "Bitmap Button", c4d.BFH_CENTER, 0, 0, self.buttonBC("", "Preset0"))
        self.LogoButton7.SetImage(self.img_btnAutoImportOff_PROP, True)  # Add the image to the button
        self.auto_import_prop_but = self.LogoButton7

        self.GroupEnd()  # END ///////////////////////////////////////////////
        self.AddSeparatorV(0, c4d.BFV_SCALEFIT)  # Separator V


        self.LogoButton6 = self.AddCustomGui(self.BUTTON_AUTO_IK, c4d.CUSTOMGUI_BITMAPBUTTON, "Bitmap Button", c4d.BFH_CENTER, 0, 0, self.buttonBC("", "Preset0"))
        self.LogoButton6.SetImage(self.img_btnAutoIK, True)  # Add the image to the button
        self.auto_ik_but = self.LogoButton6


        self.GroupEnd()  # END ///////////////////////////////////////////////
        self.GroupEnd()  # END ///////////////////////////////////////////////
    
        self.GroupEnd()  # END ///////////////////////////////////////////////

        self.AddSeparatorH(c4d.BFV_SCALEFIT)  # Separator H

        self.GroupBegin(10000, c4d.BFH_SCALEFIT, 1, title='Materials:') #MATERIALS BEGIN -----------------------------------------------------
        self.GroupBorder(c4d.BORDER_OUT)
        self.GroupBorderSpace(10, 0, 10, 10)

        self.GroupBegin(10000, c4d.BFH_SCALEFIT, 3)  # BEGIN ----------------------
        self.GroupBorderNoTitle(c4d.BORDER_NONE)
        self.GroupBorderSpace(20, 5, 20, 5)

        self.LogoButton6 = self.AddCustomGui(self.BUTTON_CONVERT_MATERIALS, c4d.CUSTOMGUI_BITMAPBUTTON, "Bitmap Button", c4d.BFH_CENTER, 0, 0, self.buttonBC("", "Preset0"))
        self.LogoButton6.SetImage(self.img_btnConvertMaterials, True)  # Add the image to the button
        self.convert_mat_but = self.LogoButton6
        self.AddSeparatorV(0, c4d.BFV_SCALEFIT)  # Separator V
        self.AddComboBox(2001, c4d.BFH_SCALEFIT, 100, 15, False)
        self.AddChild(2001, 0, ' - Select -')
        self.AddChild(2001, 1, 'V-Ray')
        self.AddChild(2001, 2, 'Redshift')
        self.AddChild(2001, 3, 'Octane')

        self.GroupEnd()  # END ///////////////////////////////////////////////


        self.GroupBegin(10000, c4d.BFH_SCALEFIT, 2, title='Global Skin Parameters:')  # BEGIN ----------------------
        self.GroupBorder(c4d.BORDER_THIN_OUT)
        self.GroupBorderSpace(20, 5, 20, 5)

        self.AddStaticText(99, c4d.BFH_CENTER, 0, 0, name='Specular Weight:')
        self.AddEditSlider(17524, c4d.BFH_SCALEFIT, initw=40, inith=0)
        self.SetInt32(17524, value=20, min=0, max=100)

        self.AddStaticText(99, c4d.BFH_CENTER, 0, 0, name='Specular Roughtness:')
        self.AddEditSlider(17525, c4d.BFH_SCALEFIT, initw=40, inith=0)
        self.SetInt32(17525, value=57, min=0, max=100)

        self.GroupEnd()  # END ///////////////////////////////////////////////

        self.GroupBegin(10001, c4d.BFH_CENTER, 2, title="Redshift Settings: ")
        self.GroupBorder(c4d.BORDER_THIN_OUT)
        self.GroupBorderSpace(20, 5, 20, 5)
        self.AddStaticText(99, c4d.BFH_CENTER, 0, 0, name='Choose Bump Type:')
        self.AddComboBox(2002,c4d.BFH_SCALEFIT, 0, 0, False)
        self.AddChild(2002, 0, 'Tangent-Space Normal')
        self.AddChild(2002, 1, 'Bump/Height Field')
        self.AddChild(2002, 2, 'Object-Space Normal')
        self.GroupEnd()

        self.GroupEnd() # MATERIALS END ///////////////////////////////////////////////

        self.AddSeparatorH(c4d.BFV_SCALEFIT)  # Separator H

        self.GroupBegin(10000, c4d.BFH_CENTER, 2, title='Global Skin Parameters:')  # BEGIN ----------------------
        self.GroupBegin(10001, c4d.BFH_CENTER, 2, title="Redshift Settings: ")
        self.AddStaticText(99, c4d.BFH_SCALEFIT, 0, 0, name='Copyright(c) 2020. All Rights Reserved.')

        self.LogoButtonHelp = self.AddCustomGui(self.BUTTON_HELP, c4d.CUSTOMGUI_BITMAPBUTTON, "Bitmap Button", c4d.BFH_CENTER, 0, 0, self.buttonBC("Help", "Preset0"))
        self.LogoButtonHelp.SetImage(self.img_d2c4dHelp, True)  # Add the image to the button

        self.GroupEnd()
        self.AddSeparatorH(c4d.BFV_SCALEFIT)  # Separator H

        return True

    def Command(self, id, msg):

        if id == 17524:
            slider_value = self.GetFloat(17524)
            DazToC4D().matSetSpec('Weight', slider_value)
            c4d.EventAdd()

        if id == 17525:
            slider_value = self.GetFloat(17525)
            print(slider_value/100)
            DazToC4D().matSetSpec('Rough', slider_value)
            c4d.EventAdd()  

        if id == self.BUTTON_AUTO_IMPORT_FIG:
            DazToC4D().genesisImport()

        if id == self.BUTTON_AUTO_IK:

            try:
                guiDazToC4DExtraDialog.Close()
            except:
                print('Extra Dialog Close Error...')
            doc = documents.GetActiveDocument()
            obj = doc.GetFirstObject()
            scene = ObjectIterator(obj)
            hipFound = False
            IKFound = False

            for obj in scene:
                if 'hip' in obj.GetName():
                    hipFound = True
                if 'Foot_PlatformBase' in obj.GetName():
                    IKFound = True

            if hipFound == False:
                gui.MessageDialog('No rig found to apply IK, Auto-Import a Figure and try again.', c4d.GEMB_OK)
                return 0
            else:
                if IKFound == True:
                    gui.MessageDialog('IK Already Found, Auto-Import and try again.', c4d.GEMB_OK)
                    return 0
                else:
                    if DazToC4D().findMesh() == False:
                        gui.MessageDialog('No Figure found, Auto-Import a Figure and try again.', c4d.GEMB_OK)
                    else:
                        DazToC4D().checkIfPosedResetPose() #THIS RUNS AUTO-IK !

            self.buttonsChangeState(True)

        if id == self.BUTTON_CONFIG:
            if self.extraDialog != None:
                self.extraDialog.Close()
            if self.extraDialog == None:
                self.extraDialog = EXTRADialog()
                guiDazToC4DExtraDialog = self.extraDialog
            self.extraDialog = EXTRADialog()

            guiDazToC4DExtraDialog = self.extraDialog
            self.extraDialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, xpos=-1, ypos=-1, defaultw=200, defaulth=150)

            '''

            '''

        if id == self.BUTTON_CONVERT_MATERIALS:
            #CONVERT MATERIAL
            doc = c4d.documents.GetActiveDocument()
            comboRender = self.GetInt32(2001)
            redshiftBumpType = self.GetInt32(2002)
            if comboRender == 0:
                gui.MessageDialog('Please select renderer from the list')

            else:
                if DazToC4D().checkStdMats() == True:
                    return
                else:
                    answer = gui.MessageDialog('::: WARNING :::\n\nNo Undo for this.\nSave your scene first, in case you want to revert changes.\n\nProceed and Convert Materials now?', c4d.GEMB_YESNO)
                    if answer is 6:
                        if comboRender == 1:
                            convertMaterials().convertTo('Vray')
                            c4d.CallCommand(1026375)  # Reload Python Plugins

                        if comboRender == 2:
                            convert_to_redshift = convertToRedshift()
                            convert_to_redshift.getBumpType(redshiftBumpType)
                            convert_to_redshift.execute()
                            DazToC4D().hideEyePolys()
                            c4d.CallCommand(100004766, 100004766)  # Select All
                            c4d.CallCommand(100004767, 100004767)  # Deselect All

                        if comboRender == 3:
                            Materials.Materials().convertToOctane()
                            DazToC4D().hideEyePolys()
                            c4d.CallCommand(100004766, 100004766)  # Select All
                            c4d.CallCommand(100004767, 100004767)  # Deselect All

        if id == self.BUTTON_TEMP:
            if self.dialog == None:
                self.dialog = EXTRADialog()
            self.dialog = EXTRADialog()
            self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, xpos=-1, ypos=-1, pluginid=103299851, defaultw=200, defaulth=150)

        if id == self.BUTTON_HELP:
            new = 2  # open in a new tab, if possible
            url = "http://www.daz3d.com"
            webbrowser.open(url, new=new)


        return True
