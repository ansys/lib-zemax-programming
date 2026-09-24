using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZOSAPI;
using ZOSAPI.Analysis;
using ZOSAPI.Common;

namespace RadianceCamera
{
    public partial class setting_dialog : Form
    {
        ISettingsData TheSettings;
        IOpticalSystem TheSystem;
        IUserAnalysisData TheAnalysisData;
        public setting_dialog(ISettingsData receive_TheSettings, IOpticalSystem receive_TheSystem)
        {
            TheSettings = receive_TheSettings;
            TheSystem = receive_TheSystem;
            TheAnalysisData = TheSystem.TheApplication.UserAnalysisData;
            InitializeComponent();
        }
        private void setting_dialog_Load(object sender, EventArgs e)
        {
            // Get parameters
            int xpix, ypix, objnum, wavnum, smooth;
            double xwid, ywid, tarz;
            string sourcepath;
            bool islog, isirr;
            if (!TheSettings.GetIntegerValue("xpix", out xpix))
                return;
            TheSettings.GetIntegerValue("ypix", out ypix);
            TheSettings.GetIntegerValue("objnum", out objnum);
            TheSettings.GetIntegerValue("wavnum", out wavnum);
            TheSettings.GetIntegerValue("smooth", out smooth);
            TheSettings.GetDoubleValue("xwid", out xwid);
            TheSettings.GetDoubleValue("ywid", out ywid);
            TheSettings.GetDoubleValue("tarz", out tarz);
            TheSettings.GetStringValue("sourcepath", out sourcepath);
            TheSettings.GetBooleanValue("islog", out islog);
            TheSettings.GetBooleanValue("isirr", out isirr);

            tb_xpix.Text = xpix.ToString();
            tb_ypix.Text = ypix.ToString();
            tb_objnum.Text = objnum.ToString();
            tb_wavnum.Text = wavnum.ToString();
            tb_smooth.Text = smooth.ToString();
            tb_ywid.Text = ywid.ToString();
            tb_xwid.Text = xwid.ToString();
            tb_targetz.Text = tarz.ToString();
            tb_sourcpath.Text = sourcepath.ToString();
            chk_islog.Checked = islog;
            chk_PSA.Checked = isirr;
        }

        void set_parameters()
        {
            // Get parameters
            int xpix, ypix, objnum, wavnum, smooth;
            double xwid, ywid, tarz;
            xpix = int.Parse(tb_xpix.Text);
            ypix = int.Parse(tb_ypix.Text);
            objnum = int.Parse(tb_objnum.Text);
            wavnum = int.Parse(tb_wavnum.Text);
            smooth = int.Parse(tb_smooth.Text);
            xwid = double.Parse(tb_xwid.Text);
            ywid = double.Parse(tb_ywid.Text);
            tarz = double.Parse(tb_targetz.Text);

            // check data
            TheSettings.SetIntegerValue("xpix", xpix);
            TheSettings.SetIntegerValue("ypix", ypix);
            TheSettings.SetIntegerValue("objnum", objnum);
            TheSettings.SetIntegerValue("wavnum", wavnum);
            TheSettings.SetIntegerValue("smooth", smooth);
            TheSettings.SetDoubleValue("xwid", xwid);
            TheSettings.SetDoubleValue("ywid", ywid);
            TheSettings.SetDoubleValue("tarz", tarz);
            TheSettings.SetStringValue("sourcepath", tb_sourcpath.Text);
            TheSettings.SetBooleanValue("islog", chk_islog.Checked);
            TheSettings.SetBooleanValue("isirr", chk_PSA.Checked);
        }

        private void bt_load_Click(object sender, EventArgs e)
        {
            // Get file path
            OpenFileDialog sfd = new OpenFileDialog
            {
                Title = "Load source file",
                Filter = "Zemax Source File (.dat;.sdf) |*.dat;*.sdf",
                InitialDirectory = TheSystem.TheApplication.ZemaxDataDir + "\\Objects\\Sources\\Source Files\\",
                ShowHelp = true
            };
            sfd.ShowDialog();

            tb_sourcpath.Text = sfd.FileName;
        }

        private void tb_xwid_Validating(object sender, CancelEventArgs e)
        {
            double parsed;
            if (Double.TryParse(tb_xwid.Text, out parsed) && parsed > 0)
                tb_xwid.Text = parsed.ToString();
            else
                tb_xwid.Text = "1";
        }

        private void tb_ywid_Validating(object sender, CancelEventArgs e)
        {
            double parsed;
            if (Double.TryParse(tb_ywid.Text, out parsed) && parsed > 0)
                tb_ywid.Text = parsed.ToString();
            else
                tb_ywid.Text = "1";
        }

        private void tb_xpix_Validating(object sender, CancelEventArgs e)
        {
            int parsed;
            if (Int32.TryParse(tb_xpix.Text, out parsed) && parsed > 0)
                tb_xpix.Text = parsed.ToString();
            else
                tb_xpix.Text = "100";
        }

        private void tb_ypix_Validating(object sender, CancelEventArgs e)
        {
            int parsed;
            if (Int32.TryParse(tb_ypix.Text, out parsed) && parsed > 0)
                tb_ypix.Text = parsed.ToString();
            else
                tb_ypix.Text = "100";
        }

        private void tb_targetz_Validating(object sender, CancelEventArgs e)
        {
            double parsed;
            if (Double.TryParse(tb_targetz.Text, out parsed) && parsed > 0)
                tb_targetz.Text = parsed.ToString();
            else
                tb_targetz.Text = "100";
        }

        private void tb_objnum_Validating(object sender, CancelEventArgs e)
        {
            int parsed;
            if (Int32.TryParse(tb_objnum.Text, out parsed) && parsed > 0 && parsed <= TheSystem.NCE.NumberOfObjects)
                tb_objnum.Text = parsed.ToString();
            else
                tb_objnum.Text = "1";
        }
        private void tb_wavnum_Validating(object sender, CancelEventArgs e)
        {
            int parsed;
            if (Int32.TryParse(tb_wavnum.Text, out parsed) && parsed >= -1 && parsed <= TheSystem.SystemData.Wavelengths.NumberOfWavelengths)
                tb_wavnum.Text = parsed.ToString();
            else
                tb_wavnum.Text = "0";
        }
        private void tb_smooth_Validating(object sender, CancelEventArgs e)
        {
            int parsed;
            if (Int32.TryParse(tb_smooth.Text, out parsed) && parsed > 0)
                tb_smooth.Text = parsed.ToString();
            else
                tb_smooth.Text = "0";
        }

        private void bt_OK_Click(object sender, EventArgs e)
        {
            set_parameters();
            this.Close();
        }

        private void bt_applybt_apply_Click(object sender, EventArgs e)
        {
            set_parameters();
            TheAnalysisData.RunAnalysisOnSettingsClosed = true;
            this.Close();
        }

        private void bt_cancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void bt_tip_Click(object sender, EventArgs e)
        {
            System.Windows.Forms.MessageBox.Show(
                "This tool calculate radiance/luminance on a distant plane seen by a humany eye.\n\n" +
                "How to use:\n\n" +
                "0. This tool is not comprehensively tested via QA process and can be unstable. Contact Ansys Support if there is any questions.\n\n" +
                "1. Setup an Annulus object in the system, which is your \"eye pupi\". Minimum X/Y Width should be always zero. Maximum X/Y Width should be same.\n\n" +
                "2. Note this tool assumes rays are from -z and propagate in +z relative to the Annulus' local coordinatel.\n\n" +
                "3. Now trace rays with saving rays hitting Annulus as source file. That means in Ray Trace Control dialog, you will set something like \"##-abcd.sdf\", where ## is Annulus object number, abcd is filename, .sdf is extention filename, which can be .dat instead.\n\n" +
                "4. Then go back to this tool's settings. X/Y Pixels/Widths are the size of the plane the eye is looking at. Target Z is the distance from the eye to this plane. Note this plane is always considered as at -z side of the Annulus object.\n\n" +
                "5. The tool detects setting in System Explorer > Unit > Source Unit and show luminance or radiance correspondingly.\n" +
                "6. Wave# is only used when needed. -1 means using primary wavelenght. 0 means to use the wavelength data in the .dat file. Otherwise it's the number of system wavelengths.\n\n" +
                "7. If you check \"Log\", you can find a report in \\Zemax\\Objects\\Sources\\Source Files\\radiance_camera.log. This is mainly for debug, but it's also useful if you want to check the source content.\n\n" +
                "8. The check box \"Irradiance\" is mainly for debug, but you could use it show irradiance or illuminance on the target plane.\n\n" +
                "9. Note you must retrace and save the source file whenever you changed the Annulus object's position or orientation. The tool detects if the rays included in the source file are on the Annulus and stop if they are not.");
        }
    }
}
