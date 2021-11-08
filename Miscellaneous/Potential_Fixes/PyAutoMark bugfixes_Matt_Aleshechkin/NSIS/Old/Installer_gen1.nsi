; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "PyAutoMark"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\PyAutoMark.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; MUI 1.67 compatible ------
!include "MUI.nsh"
Unicode True

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\Application\icon.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "..\Application\License.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
;!define MUI_FINISHPAGE_RUN "$INSTDIR\PyAutoMark.exe" # this only works if "Enable Protected Mode at startup" is disabled in Acrobat Reader, so it's not for sure (PDF will fail)
;!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\PyAutoMark_Documentation.pdf" # this only works if "Enable Protected Mode at startup" is disabled in Acrobat Reader, so it's not for sure
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "PyAutoMark_Installer.exe"
RequestExecutionLevel admin # added after using HM NIS Edit
InstallDir "$PROGRAMFILES\PyAutoMark"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR\build\PyAutoMark"
  SetOverwrite try
  File "..\Application\build\PyAutoMark\Analysis-00.toc"
  File "..\Application\build\PyAutoMark\base_library.zip"
  File "..\Application\build\PyAutoMark\EXE-00.toc"
  File "..\Application\build\PyAutoMark\PKG-00.pkg"
  File "..\Application\build\PyAutoMark\PKG-00.toc"
  File "..\Application\build\PyAutoMark\PyAutoMark.exe.manifest"
  File "..\Application\build\PyAutoMark\PYZ-00.pyz"
  File "..\Application\build\PyAutoMark\PYZ-00.toc"
  File "..\Application\build\PyAutoMark\Tree-00.toc"
  File "..\Application\build\PyAutoMark\Tree-01.toc"
  File "..\Application\build\PyAutoMark\Tree-02.toc"
  File "..\Application\build\PyAutoMark\warn-PyAutoMark.txt"
  File "..\Application\build\PyAutoMark\xref-PyAutoMark.html"
  SetOutPath "$INSTDIR"
  File "..\Application\config.json"
  SetOutPath "$INSTDIR\Examples\Assignment_Solutions"
  File "..\Application\Examples\Assignment_Solutions\A1_key.py"
  File "..\Application\Examples\Assignment_Solutions\doc_key.py"
  SetOutPath "$INSTDIR\Examples\Student_Submissions\Assignment1_complete"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\A1_Bob.zip"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\A1_Dan.zip"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\A1_Dylan.zip"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\A1_Jo.zip"
  SetOutPath "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\Output_Summaries"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Bob.txt"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Dan.txt"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Dylan.txt"
  File "..\Application\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Jo.txt"
  SetOutPath "$INSTDIR\Examples\Student_Submissions\Assignment1_doc"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\A1_Arthas.zip"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\A1_Bob.zip"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\A1_Dan.zip"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\A1_Dylan.zip"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\A1_Jo.zip"
  SetOutPath "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\Output_Summaries"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Arthas.txt"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Bob.txt"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Dan.txt"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Dylan.txt"
  File "..\Application\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Jo.txt"
  SetOutPath "$INSTDIR"
  File "..\Application\icon.ico"
  File "..\Application\License.txt"
  File "..\Application\PyAutoMark.exe"
  CreateDirectory "$SMPROGRAMS\PyAutoMark"
  CreateShortCut "$SMPROGRAMS\PyAutoMark\PyAutoMark.lnk" "$INSTDIR\PyAutoMark.exe"
  CreateShortCut "$DESKTOP\PyAutoMark.lnk" "$INSTDIR\PyAutoMark.exe"
  File "..\Application\PyAutoMark.py"
  File "..\Application\PyAutoMark.spec"
  File "..\Application\PyAutoMark_Documentation.pdf"
SectionEnd

Section -AdditionalIcons
  CreateShortCut "$SMPROGRAMS\PyAutoMark\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\PyAutoMark.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\PyAutoMark.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\PyAutoMark_Documentation.pdf"
  Delete "$INSTDIR\PyAutoMark.spec"
  Delete "$INSTDIR\PyAutoMark.py"
  Delete "$INSTDIR\PyAutoMark.exe"
  Delete "$INSTDIR\License.txt"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Jo.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Dylan.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Dan.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Bob.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\Output_Summaries\A1_Arthas.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\A1_Jo.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\A1_Dylan.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\A1_Dan.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\A1_Bob.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\A1_Arthas.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Jo.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Dylan.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Dan.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\Output_Summaries\A1_Bob.txt"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\A1_Jo.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\A1_Dylan.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\A1_Dan.zip"
  Delete "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\A1_Bob.zip"
  Delete "$INSTDIR\Examples\Assignment_Solutions\doc_key.py"
  Delete "$INSTDIR\Examples\Assignment_Solutions\A1_key.py"
  Delete "$INSTDIR\config.json"
  Delete "$INSTDIR\build\PyAutoMark\xref-PyAutoMark.html"
  Delete "$INSTDIR\build\PyAutoMark\warn-PyAutoMark.txt"
  Delete "$INSTDIR\build\PyAutoMark\Tree-02.toc"
  Delete "$INSTDIR\build\PyAutoMark\Tree-01.toc"
  Delete "$INSTDIR\build\PyAutoMark\Tree-00.toc"
  Delete "$INSTDIR\build\PyAutoMark\PYZ-00.toc"
  Delete "$INSTDIR\build\PyAutoMark\PYZ-00.pyz"
  Delete "$INSTDIR\build\PyAutoMark\PyAutoMark.exe.manifest"
  Delete "$INSTDIR\build\PyAutoMark\PKG-00.toc"
  Delete "$INSTDIR\build\PyAutoMark\PKG-00.pkg"
  Delete "$INSTDIR\build\PyAutoMark\EXE-00.toc"
  Delete "$INSTDIR\build\PyAutoMark\base_library.zip"
  Delete "$INSTDIR\build\PyAutoMark\Analysis-00.toc"

  Delete "$SMPROGRAMS\PyAutoMark\Uninstall.lnk"
  Delete "$DESKTOP\PyAutoMark.lnk"
  Delete "$SMPROGRAMS\PyAutoMark\PyAutoMark.lnk"

  RMDir "$SMPROGRAMS\PyAutoMark"
  RMDir "$INSTDIR\Examples\Student_Submissions\Assignment1_doc\Output_Summaries"
  RMDir "$INSTDIR\Examples\Student_Submissions\Assignment1_doc"
  RMDir "$INSTDIR\Examples\Student_Submissions\Assignment1_complete\Output_Summaries"
  RMDir "$INSTDIR\Examples\Student_Submissions\Assignment1_complete"
  RMDir "$INSTDIR\Examples\Student_Submissions"
  RMDir "$INSTDIR\Examples\Assignment_Solutions"
  RMDir "$INSTDIR\Examples"
  RMDir "$INSTDIR\build\PyAutoMark"
  RMDir "$INSTDIR\build"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd