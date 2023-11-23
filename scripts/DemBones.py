import hou
import subprocess
import os
import zipfile
import platform
import ntpath


def unzip_file(zip_file, destination_path):
    with zipfile.ZipFile(zip_file, 'r', zipfile.ZIP_DEFLATED) as zipf:
        zipf.extractall(destination_path)


def Convert(kwargs):
    node = kwargs['node']

    ABCFile = node.parm("sAnimatedCache").evalAsString()
    BindPoseFile = node.parm("sBindPoseFBX").evalAsString()
    ExportFile = node.parm('sExportFile').evalAsString()

    SIDEFXLABSDIR = hou.text.expandString('$SIDEFXLABS')
    ExecutableDir = node.parm("executablecache").evalAsString()

    ZipPath = os.path.join(SIDEFXLABSDIR, "misc", "dem-bones", "DemBones.zip")
    DemBonesExe = os.path.join(ExecutableDir, "misc", "dem-bones", "DemBones")

    # Find the right executable based on OS
    OS = platform.system()
    if OS == "Windows":
        DemBonesExe += "-Windows.exe"
    elif OS == "Linux":
        DemBonesExe += "-Linux"
    else:
        DemBonesExe += "-Darwin"

    head, tail = ntpath.split(ExportFile)
    if not os.path.exists(head):
        os.makedirs(head)

    if not os.path.exists(DemBonesExe):
        unzip_file(ZipPath, os.path.join(ExecutableDir, "misc", "dem-bones"))

    if not os.path.exists(DemBonesExe):
        raise hou.NodeError("The executable for Dem Bones cannot be found")

    # Popup Dialog
    with hou.InterruptableOperation(node.name(), open_interrupt_dialog=True) as Operation:

        # Render the temp files
        node.node("rop_alembic1").render()
        node.node("rop_fbx1").render()

        # Hide popup dialog
        StartupInfo = None

        if os.name == 'nt' and node.parm("bHideShell").evalAsInt() == 1:
            StartupInfo = subprocess.STARTUPINFO()
            subprocess.STARTF_USESHOWWINDOW = 1
            StartupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Construct Commandline Arguments
        parms = ['nBones', 'nIters', 'nInitIters', 'nTransIters', 'transAffine', 'transAffineNorm', 'nWeightsIters',
                 'weightsSmooth', 'weightsSmoothStep', 'nnz', 'patience', 'tolerance']
        cmd = [DemBonesExe, "--init={0}".format(BindPoseFile), "--abc={0}".format(ABCFile),
               "--out={0}".format(ExportFile)]

        for parm in parms:
            cmd.append('--{0}={1}'.format(parm, node.parm(parm).evalAsString()))

        if node.parm("createroot").evalAsInt() == 1:
            cmd.append("--bindUpdate=2")

        # Starting the process
        with subprocess.Popen(cmd, startupinfo=StartupInfo) as Process:

            # Process is still running
            while Process.poll() is None:
                try:
                    Operation.updateProgress(0.0)
                # User interrupted
                except hou.OperationInterrupted:
                    Process.kill()

        # Cleanup
        if os.path.exists(ABCFile):
            os.remove(ABCFile)
        if os.path.exists(BindPoseFile):
            os.remove(BindPoseFile)





