using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CSharpUserExtensionApplication
{
    public partial class ExtensionSettingsForm : Form
    {        
        private int _WaveNumber;
        private double _Apodization_G;
        private double _Input_NAx, _Input_NAy;
        private double angle_x, angle_y;
        private double waist_x, waist_y;

        private double _ObjectNA;
        private double _Input_VCX, _Input_VCY;

        private double _Check_NA;
        private double _Check_G;
        private double _Check_VCX, _Check_VCY;


        public ExtensionSettingsForm()
        {
            InitializeComponent();

            // This loads up the settings form, and populates the settings with the specified values
            // Put all intialization scripts in here (including loading setting values from previous run)
            // Create a connection to OpticStudio in order to get information from 'Program.cs'
            ZOSAPI.ZOSAPI_Connection TheConnection = new ZOSAPI.ZOSAPI_Connection();
            ZOSAPI.IZOSAPI_Application TheApplication = TheConnection.ConnectToApplication();
            ZOSAPI.IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            this.AcceptButton = button2;  //button Calculate from tab Input
            this.AcceptButton = button4;  //button Calculate from tab Check


            // Generate a list of possible surfaces (i.e. not ignored) for the Object setting combo-box
            // There must be at least 1 valid surface, otherwise Program.c would have errored out                        
            for (int i = 1; i <= TheApplication.PrimarySystem.SystemData.Wavelengths.NumberOfWavelengths; i++)
            {
                double wavelength = TheApplication.PrimarySystem.SystemData.Wavelengths.GetWavelength(i).Wavelength;
                cb_WaveNum.Items.Add(wavelength);
                cb_WaveNum2.Items.Add(wavelength);
            }
            cb_definition.Items.Add("NA");
            cb_definition.Items.Add("Waist");
            cb_definition.Items.Add("Divergence in degrees");
            
            // Set some initial values for settings data (same intial values as in Program.cs)            
            double initial_G = 2;
            //Input
            int initial_WaveNumber = 0;
            int initial_definition = 0;
            double initial_NAx = 0.1;
            double initial_NAy = 0.2;            
            //Check            
            double initial_VCx = 0.51;
            double initial_VCy = 0.0;            
            double initial_ObjectNA = 0.28;

            // Populate the settings form with the set values   
            //Input
            cb_WaveNum.SelectedIndex = initial_WaveNumber;            
            cb_definition.SelectedIndex = initial_definition;
            textBox_NAx_Input.Text = Convert.ToString(initial_NAx);
            textBox_NAy_Input.Text = Convert.ToString(initial_NAy);
            textBox_G_Input.Text = Convert.ToString(initial_G);
            label7.Text = "";// (Intensity of marginal ray (exp(-2G)))";
            label_Intensity_Input.Text = "";
            //Check
            cb_WaveNum2.SelectedIndex = initial_WaveNumber;
            textBox_G_Check.Text = Convert.ToString(initial_G);
            textBox_NA_Check.Text = Convert.ToString(initial_ObjectNA);            
            textBox_VCX_Check.Text = Convert.ToString(initial_VCx);
            textBox_VCY_Check.Text = Convert.ToString(initial_VCy);

        }

        private void ExtensionSettingsForm_Load(object sender, EventArgs e)
        {

        }

        //Input tab: we are creating parameters to set-up properly OpticStudio
        private void button2_Click(object sender, EventArgs e)
        {
            
        }

        //Check tab: we are checking that OpticStudio is properly set-up
        //Check that a file is correctly set up
        private void button4_Click(object sender, EventArgs e)
        {
        }



        // Get & set surface number              
        public int WaveNumber
        {
            get { return _WaveNumber; }
            set { _WaveNumber = value; }
        }

        public double Apodization_G
        {
            get { return _Apodization_G; }
            set { _Apodization_G = value; }
        }

        

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void ExtensionSettingsForm_Load_1(object sender, EventArgs e)
        {

        }

        
        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        

        private void label8_Click(object sender, EventArgs e)
        {

        }

        private void Input_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void fileSystemWatcher1_Changed(object sender, System.IO.FileSystemEventArgs e)
        {

        }

        private void tabPage1_Click(object sender, EventArgs e)
        {

        }

        private void tabPage2_Click(object sender, EventArgs e)
        {

        }

        private void label20_Click(object sender, EventArgs e)
        {

        }

        private void label19_Click(object sender, EventArgs e)
        {

        }

        private void label10_Click(object sender, EventArgs e)
        {

        }

        private void label18_Click(object sender, EventArgs e)
        {

        }

        private void label9_Click(object sender, EventArgs e)
        {

        }

        private void label17_Click(object sender, EventArgs e)
        {

        }

        private void label8_Click_1(object sender, EventArgs e)
        {

        }
               
        private void label7_Click(object sender, EventArgs e)
        {

        }

        private void label16_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void label15_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label14_Click(object sender, EventArgs e)
        {

        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void tb_s1tow_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void label13_Click(object sender, EventArgs e)
        {

        }

        private void tb_waist_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void label12_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click_1(object sender, EventArgs e)
        {

        }

        private void label11_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click_1(object sender, EventArgs e)
        {

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click_1(object sender, EventArgs e)
        {

        }

        private void cb_WaveNum_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        

        private void textBox_G_Input_TextChanged(object sender, EventArgs e)
        {

        }

        private void label2_Click_2(object sender, EventArgs e)
        {

        }

        private void label22_Click(object sender, EventArgs e)
        {

        }

        private void cb_WaveNum2_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            double max_NA;
            double valuex, valuey;


            // This is run when the user hits "OK"    
            double wavelength = Convert.ToDouble(cb_WaveNum.SelectedItem);
            _WaveNumber = (int)cb_WaveNum.SelectedIndex;

            valuex = Convert.ToDouble(textBox_NAx_Input.Text);
            valuey = Convert.ToDouble(textBox_NAy_Input.Text);


            if (cb_definition.SelectedIndex == 0) //NA
            {
                _Input_NAx = valuex;
                _Input_NAy = valuey;
                angle_x = Math.Asin(_Input_NAx); //angle_x in radians
                angle_y = Math.Asin(_Input_NAy); //angle_y in radians
                waist_x = wavelength / ((Math.PI) * Math.Tan(angle_x));
                waist_y = wavelength / ((Math.PI) * Math.Tan(angle_y));
            }
            if (cb_definition.SelectedIndex == 1) //waist
            {
                waist_x = valuex;
                waist_y = valuey;
                angle_x = Math.Atan2(wavelength, ((Math.PI) * waist_x)); //angle_x in radians
                angle_y = Math.Atan2(wavelength, ((Math.PI) * waist_y)); //angle_y in radians
                _Input_NAx = Math.Sin(angle_x);
                _Input_NAy = Math.Sin(angle_y);

            }
            if (cb_definition.SelectedIndex == 2) //divergence in degrees
            {
                angle_x = valuex * Math.PI / 180; //angle_x in radians
                angle_y = valuey * Math.PI / 180; //angle_y in radians
                _Input_NAx = Math.Sin(angle_x);
                _Input_NAy = Math.Sin(angle_y);
                waist_x = wavelength / (Math.PI) * Math.Tan(angle_x);
                waist_y = wavelength / (Math.PI) * Math.Tan(angle_y);
            }


            _Apodization_G = Convert.ToDouble(textBox_G_Input.Text);

            max_NA = Math.Max(_Input_NAx, _Input_NAy);
            _ObjectNA = Math.Sin(Math.Atan(Math.Sqrt(_Apodization_G) * Math.Tan(Math.Asin(max_NA))));

            double intensity = Math.Exp(-2 * _Apodization_G);
            label7.Text = "(Intensity of marginal ray (exp(-2G)))";
            label_Intensity_Input.Text = intensity.ToString("0.00%");


            label_ObjectNA_Input.Text = _ObjectNA.ToString("0.00");

            if (_Input_NAx > _Input_NAy)
            {
                _Input_VCX = 0.0;
                _Input_VCY = 1 - (Math.Tan(Math.Asin(_Input_NAy))) / (Math.Tan(Math.Asin(_Input_NAx)));
            }
            else
            {
                _Input_VCX = 1 - (Math.Tan(Math.Asin(_Input_NAx))) / (Math.Tan(Math.Asin(_Input_NAy)));
                _Input_VCY = 0.0;
            }
            label_VCX_Input.Text = _Input_VCX.ToString("0.00");
            label_VCY_Input.Text = _Input_VCY.ToString("0.00");

            label_AngleX_Input.Text = ((180 / Math.PI) * angle_x).ToString("0.00");
            label_AngleY_Input.Text = ((180 / Math.PI) * angle_y).ToString("0.00");

            label_WaistX_Input.Text = waist_x.ToString("0.0000");
            label_WaistY_Input.Text = waist_y.ToString("0.0000");

            DialogResult = DialogResult.OK;
            //Close();

        }

        private void button4_Click_1(object sender, EventArgs e)
        {
            double max_NA;
            double NAx;
            double NAy;

            // This is run when the user hits "OK"    
            double wavelength = Convert.ToDouble(cb_WaveNum.SelectedItem);


            _WaveNumber = (int)cb_WaveNum.SelectedIndex;
            _Check_NA = Convert.ToDouble(textBox_NA_Check.Text);
            _Check_G = Convert.ToDouble(textBox_G_Check.Text);
            _Check_VCX = Convert.ToDouble(textBox_VCX_Check.Text);
            _Check_VCY = Convert.ToDouble(textBox_VCY_Check.Text);

            //Need to check input data to avoid crash
            /*Idea to improve if text is empty
            if (double.TryParse(textBox_NA_Check.Text, out _Check_NA))
            {

            }
            */

            max_NA = Math.Sin(Math.Atan((1 / Math.Sqrt(_Check_G)) * Math.Tan(Math.Asin(_Check_NA))));

            //Check if one of the vignetting factors is set to 0
            if ((_Check_VCX != 0) && (_Check_VCY != 0))
            {
                //display an error message
                MessageBox.Show("VCX or VCY must be equal to 0", "Wrong Input", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            if (_Check_VCY==0) //There is a vignetting factor for X
            {
                NAy = max_NA;
                NAx = Math.Sin(Math.Atan((1 - _Check_VCX) * Math.Tan(Math.Asin(NAy))));
            }
            else
            {
                NAx = max_NA;
                NAy = Math.Sin(Math.Atan((1 - _Check_VCY) * Math.Tan(Math.Asin(NAx))));
            }
            label_NAX_Check.Text = NAx.ToString("0.00");
            label_NAY_Check.Text = NAy.ToString("0.00");

            double angle_x = Math.Asin(NAx); //angle_x in radians
            double angle_y = Math.Asin(NAy); //angle_y in radians
            double waist_x = wavelength / ((Math.PI) * Math.Tan(angle_x));
            double waist_y = wavelength / ((Math.PI) * Math.Tan(angle_y));

            label_AngleX_Check.Text = ((180 / Math.PI) * angle_x).ToString("0.00");
            label_AngleY_Check.Text = ((180 / Math.PI) * angle_y).ToString("0.00");

            label_WaistX_Check.Text = waist_x.ToString("0.0000");
            label_WaistY_Check.Text = waist_y.ToString("0.0000");

            DialogResult = DialogResult.OK;
            //Close();
        }

        private void textBox7_TextChanged(object sender, EventArgs e)
        {

        }

        private void label7_Click_1(object sender, EventArgs e)
        {

        }

        private void textBox_VCY_Check_TextChanged(object sender, EventArgs e)
        {

        }

        private void label18_Click_1(object sender, EventArgs e)
        {

        }

        private void cb_definition_SelectedIndexChanged(object sender, EventArgs e)
        {
            //cb_definition.Items.Add("NA");
            //cb_definition.Items.Add("Waist");
            //cb_definition.Items.Add("Divergence in degrees");


            if (cb_definition.SelectedIndex == 0) 
            {
                Definition_x.Text = "NAx (1/e^2):";
                Definition_y.Text = "NAy (1/e^2):";
            }
            if (cb_definition.SelectedIndex == 1)
            {
                Definition_x.Text = "Waistx (1/e^2) in µm:";
                Definition_y.Text = "Waisty (1/e^2) in µm::";
            }
            if (cb_definition.SelectedIndex == 2)
            {
                Definition_x.Text = "Divergencex (1/e^2) deg:";
                Definition_y.Text = "Divergencey (1/e^2) deg:";
            }

        }

    }
}
