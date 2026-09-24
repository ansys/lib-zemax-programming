namespace CSharpUserExtensionApplication
{
    partial class ExtensionSettingsForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.fileSystemWatcher1 = new System.IO.FileSystemWatcher();
            this.Input = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.button2 = new System.Windows.Forms.Button();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.label_WaistY_Input = new System.Windows.Forms.Label();
            this.label_WaistX_Input = new System.Windows.Forms.Label();
            this.label_AngleY_Input = new System.Windows.Forms.Label();
            this.label_AngleX_Input = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.label_Intensity_Input = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label_ObjectNA_Input = new System.Windows.Forms.Label();
            this.label17 = new System.Windows.Forms.Label();
            this.textBox_G_Input = new System.Windows.Forms.TextBox();
            this.label13 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.label_VCX_Input = new System.Windows.Forms.Label();
            this.label16 = new System.Windows.Forms.Label();
            this.label_VCY_Input = new System.Windows.Forms.Label();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.label19 = new System.Windows.Forms.Label();
            this.cb_definition = new System.Windows.Forms.ComboBox();
            this.textBox_NAy_Input = new System.Windows.Forms.TextBox();
            this.Definition_y = new System.Windows.Forms.Label();
            this.textBox_NAx_Input = new System.Windows.Forms.TextBox();
            this.Definition_x = new System.Windows.Forms.Label();
            this.label11 = new System.Windows.Forms.Label();
            this.cb_WaveNum = new System.Windows.Forms.ComboBox();
            this.tabPage3 = new System.Windows.Forms.TabPage();
            this.button4 = new System.Windows.Forms.Button();
            this.groupBox6 = new System.Windows.Forms.GroupBox();
            this.label_WaistY_Check = new System.Windows.Forms.Label();
            this.label_WaistX_Check = new System.Windows.Forms.Label();
            this.label23 = new System.Windows.Forms.Label();
            this.label24 = new System.Windows.Forms.Label();
            this.label_AngleY_Check = new System.Windows.Forms.Label();
            this.label_AngleX_Check = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.label18 = new System.Windows.Forms.Label();
            this.groupBox5 = new System.Windows.Forms.GroupBox();
            this.label_NAX_Check = new System.Windows.Forms.Label();
            this.label_NAY_Check = new System.Windows.Forms.Label();
            this.label33 = new System.Windows.Forms.Label();
            this.label21 = new System.Windows.Forms.Label();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.label30 = new System.Windows.Forms.Label();
            this.label31 = new System.Windows.Forms.Label();
            this.textBox_VCY_Check = new System.Windows.Forms.TextBox();
            this.textBox_G_Check = new System.Windows.Forms.TextBox();
            this.label34 = new System.Windows.Forms.Label();
            this.textBox_VCX_Check = new System.Windows.Forms.TextBox();
            this.textBox_NA_Check = new System.Windows.Forms.TextBox();
            this.label37 = new System.Windows.Forms.Label();
            this.label22 = new System.Windows.Forms.Label();
            this.cb_WaveNum2 = new System.Windows.Forms.ComboBox();
            ((System.ComponentModel.ISupportInitialize)(this.fileSystemWatcher1)).BeginInit();
            this.Input.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.tabPage3.SuspendLayout();
            this.groupBox6.SuspendLayout();
            this.groupBox5.SuspendLayout();
            this.groupBox4.SuspendLayout();
            this.SuspendLayout();
            // 
            // fileSystemWatcher1
            // 
            this.fileSystemWatcher1.EnableRaisingEvents = true;
            this.fileSystemWatcher1.SynchronizingObject = this;
            this.fileSystemWatcher1.Changed += new System.IO.FileSystemEventHandler(this.fileSystemWatcher1_Changed);
            // 
            // Input
            // 
            this.Input.Controls.Add(this.tabPage1);
            this.Input.Controls.Add(this.tabPage3);
            this.Input.Location = new System.Drawing.Point(-3, 2);
            this.Input.Margin = new System.Windows.Forms.Padding(4);
            this.Input.Name = "Input";
            this.Input.SelectedIndex = 0;
            this.Input.Size = new System.Drawing.Size(807, 517);
            this.Input.TabIndex = 0;
            this.Input.SelectedIndexChanged += new System.EventHandler(this.Input_SelectedIndexChanged);
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.button2);
            this.tabPage1.Controls.Add(this.groupBox3);
            this.tabPage1.Controls.Add(this.groupBox2);
            this.tabPage1.Controls.Add(this.groupBox1);
            this.tabPage1.Location = new System.Drawing.Point(4, 25);
            this.tabPage1.Margin = new System.Windows.Forms.Padding(4);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(4);
            this.tabPage1.Size = new System.Drawing.Size(799, 488);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "Set-up";
            this.tabPage1.UseVisualStyleBackColor = true;
            this.tabPage1.Click += new System.EventHandler(this.tabPage1_Click);
            // 
            // button2
            // 
            this.button2.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button2.Location = new System.Drawing.Point(299, 423);
            this.button2.Margin = new System.Windows.Forms.Padding(4);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(189, 47);
            this.button2.TabIndex = 79;
            this.button2.Text = "Calculate!";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click_1);
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.label_WaistY_Input);
            this.groupBox3.Controls.Add(this.label_WaistX_Input);
            this.groupBox3.Controls.Add(this.label_AngleY_Input);
            this.groupBox3.Controls.Add(this.label_AngleX_Input);
            this.groupBox3.Controls.Add(this.label6);
            this.groupBox3.Controls.Add(this.label5);
            this.groupBox3.Controls.Add(this.label4);
            this.groupBox3.Controls.Add(this.label3);
            this.groupBox3.Location = new System.Drawing.Point(13, 314);
            this.groupBox3.Margin = new System.Windows.Forms.Padding(4);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Padding = new System.Windows.Forms.Padding(4);
            this.groupBox3.Size = new System.Drawing.Size(756, 98);
            this.groupBox3.TabIndex = 78;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "POP";
            // 
            // label_WaistY_Input
            // 
            this.label_WaistY_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_WaistY_Input.AutoSize = true;
            this.label_WaistY_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_WaistY_Input.Location = new System.Drawing.Point(616, 57);
            this.label_WaistY_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_WaistY_Input.Name = "label_WaistY_Input";
            this.label_WaistY_Input.Size = new System.Drawing.Size(33, 21);
            this.label_WaistY_Input.TabIndex = 71;
            this.label_WaistY_Input.Text = "0.0";
            // 
            // label_WaistX_Input
            // 
            this.label_WaistX_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_WaistX_Input.AutoSize = true;
            this.label_WaistX_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_WaistX_Input.Location = new System.Drawing.Point(265, 57);
            this.label_WaistX_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_WaistX_Input.Name = "label_WaistX_Input";
            this.label_WaistX_Input.Size = new System.Drawing.Size(33, 21);
            this.label_WaistX_Input.TabIndex = 70;
            this.label_WaistX_Input.Text = "0.0";
            // 
            // label_AngleY_Input
            // 
            this.label_AngleY_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_AngleY_Input.AutoSize = true;
            this.label_AngleY_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_AngleY_Input.Location = new System.Drawing.Point(616, 28);
            this.label_AngleY_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_AngleY_Input.Name = "label_AngleY_Input";
            this.label_AngleY_Input.Size = new System.Drawing.Size(33, 21);
            this.label_AngleY_Input.TabIndex = 69;
            this.label_AngleY_Input.Text = "0.0";
            // 
            // label_AngleX_Input
            // 
            this.label_AngleX_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_AngleX_Input.AutoSize = true;
            this.label_AngleX_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_AngleX_Input.Location = new System.Drawing.Point(265, 28);
            this.label_AngleX_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_AngleX_Input.Name = "label_AngleX_Input";
            this.label_AngleX_Input.Size = new System.Drawing.Size(33, 21);
            this.label_AngleX_Input.TabIndex = 68;
            this.label_AngleX_Input.Text = "0.0";
            // 
            // label6
            // 
            this.label6.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(404, 57);
            this.label6.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(171, 21);
            this.label6.TabIndex = 67;
            this.label6.Text = "WaistY (1/e^2) in µm:";
            // 
            // label5
            // 
            this.label5.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(401, 28);
            this.label5.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(171, 21);
            this.label5.TabIndex = 66;
            this.label5.Text = "AngleY(1/e^2) in deg:";
            // 
            // label4
            // 
            this.label4.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(13, 57);
            this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(172, 21);
            this.label4.TabIndex = 65;
            this.label4.Text = "WaistX (1/e^2) in µm:";
            // 
            // label3
            // 
            this.label3.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(13, 28);
            this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(171, 21);
            this.label3.TabIndex = 64;
            this.label3.Text = "AngleX(1/e^2) in deg:";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.label7);
            this.groupBox2.Controls.Add(this.label_Intensity_Input);
            this.groupBox2.Controls.Add(this.label_ObjectNA_Input);
            this.groupBox2.Controls.Add(this.label17);
            this.groupBox2.Controls.Add(this.textBox_G_Input);
            this.groupBox2.Controls.Add(this.label13);
            this.groupBox2.Controls.Add(this.label14);
            this.groupBox2.Controls.Add(this.label_VCX_Input);
            this.groupBox2.Controls.Add(this.label16);
            this.groupBox2.Controls.Add(this.label_VCY_Input);
            this.groupBox2.Location = new System.Drawing.Point(13, 162);
            this.groupBox2.Margin = new System.Windows.Forms.Padding(4);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Padding = new System.Windows.Forms.Padding(4);
            this.groupBox2.Size = new System.Drawing.Size(756, 151);
            this.groupBox2.TabIndex = 77;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "SystemExplorer";
            // 
            // label_Intensity_Input
            // 
            this.label_Intensity_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_Intensity_Input.AutoSize = true;
            this.label_Intensity_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_Intensity_Input.Location = new System.Drawing.Point(420, 38);
            this.label_Intensity_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_Intensity_Input.Name = "label_Intensity_Input";
            this.label_Intensity_Input.Size = new System.Drawing.Size(33, 21);
            this.label_Intensity_Input.TabIndex = 73;
            this.label_Intensity_Input.Text = "0.0";
            // 
            // label7
            // 
            this.label7.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Times New Roman", 8.25F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(485, 41);
            this.label7.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(217, 16);
            this.label7.TabIndex = 72;
            this.label7.Text = "(Intensity of marginal ray (exp(-2G))";
            this.label7.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.label7.Click += new System.EventHandler(this.label7_Click_1);
            // 
            // label_ObjectNA_Input
            // 
            this.label_ObjectNA_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_ObjectNA_Input.AutoSize = true;
            this.label_ObjectNA_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_ObjectNA_Input.Location = new System.Drawing.Point(268, 74);
            this.label_ObjectNA_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_ObjectNA_Input.Name = "label_ObjectNA_Input";
            this.label_ObjectNA_Input.Size = new System.Drawing.Size(33, 21);
            this.label_ObjectNA_Input.TabIndex = 61;
            this.label_ObjectNA_Input.Text = "0.0";
            this.label_ObjectNA_Input.Click += new System.EventHandler(this.label20_Click);
            // 
            // label17
            // 
            this.label17.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label17.AutoSize = true;
            this.label17.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label17.Location = new System.Drawing.Point(16, 74);
            this.label17.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(146, 21);
            this.label17.TabIndex = 55;
            this.label17.Text = "Object Space NA:";
            this.label17.Click += new System.EventHandler(this.label17_Click);
            // 
            // textBox_G_Input
            // 
            this.textBox_G_Input.Location = new System.Drawing.Point(271, 37);
            this.textBox_G_Input.Margin = new System.Windows.Forms.Padding(4);
            this.textBox_G_Input.Name = "textBox_G_Input";
            this.textBox_G_Input.Size = new System.Drawing.Size(117, 22);
            this.textBox_G_Input.TabIndex = 3;
            this.textBox_G_Input.TextChanged += new System.EventHandler(this.textBox_G_Input_TextChanged);
            // 
            // label13
            // 
            this.label13.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label13.AutoSize = true;
            this.label13.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label13.Location = new System.Drawing.Point(16, 38);
            this.label13.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(190, 21);
            this.label13.TabIndex = 43;
            this.label13.Text = "Apodization Factor (G):";
            this.label13.Click += new System.EventHandler(this.label13_Click);
            // 
            // label14
            // 
            this.label14.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label14.AutoSize = true;
            this.label14.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label14.Location = new System.Drawing.Point(16, 114);
            this.label14.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(186, 21);
            this.label14.TabIndex = 45;
            this.label14.Text = "Vignetting Factor VCX:";
            this.label14.Click += new System.EventHandler(this.label14_Click);
            // 
            // label_VCX_Input
            // 
            this.label_VCX_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_VCX_Input.AutoSize = true;
            this.label_VCX_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_VCX_Input.Location = new System.Drawing.Point(268, 114);
            this.label_VCX_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_VCX_Input.Name = "label_VCX_Input";
            this.label_VCX_Input.Size = new System.Drawing.Size(33, 21);
            this.label_VCX_Input.TabIndex = 57;
            this.label_VCX_Input.Text = "0.0";
            this.label_VCX_Input.Click += new System.EventHandler(this.label18_Click);
            // 
            // label16
            // 
            this.label16.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label16.AutoSize = true;
            this.label16.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label16.Location = new System.Drawing.Point(401, 114);
            this.label16.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(184, 21);
            this.label16.TabIndex = 50;
            this.label16.Text = "Vignetting Factor VCY:";
            this.label16.Click += new System.EventHandler(this.label16_Click);
            // 
            // label_VCY_Input
            // 
            this.label_VCY_Input.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_VCY_Input.AutoSize = true;
            this.label_VCY_Input.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_VCY_Input.Location = new System.Drawing.Point(620, 114);
            this.label_VCY_Input.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_VCY_Input.Name = "label_VCY_Input";
            this.label_VCY_Input.Size = new System.Drawing.Size(33, 21);
            this.label_VCY_Input.TabIndex = 58;
            this.label_VCY_Input.Text = "0.0";
            this.label_VCY_Input.Click += new System.EventHandler(this.label9_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.label19);
            this.groupBox1.Controls.Add(this.cb_definition);
            this.groupBox1.Controls.Add(this.textBox_NAy_Input);
            this.groupBox1.Controls.Add(this.Definition_y);
            this.groupBox1.Controls.Add(this.textBox_NAx_Input);
            this.groupBox1.Controls.Add(this.Definition_x);
            this.groupBox1.Controls.Add(this.label11);
            this.groupBox1.Controls.Add(this.cb_WaveNum);
            this.groupBox1.Location = new System.Drawing.Point(13, 12);
            this.groupBox1.Margin = new System.Windows.Forms.Padding(4);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Padding = new System.Windows.Forms.Padding(4);
            this.groupBox1.Size = new System.Drawing.Size(756, 151);
            this.groupBox1.TabIndex = 76;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "InputBeam";
            // 
            // label19
            // 
            this.label19.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label19.AutoSize = true;
            this.label19.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label19.Location = new System.Drawing.Point(16, 70);
            this.label19.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label19.Name = "label19";
            this.label19.Size = new System.Drawing.Size(86, 21);
            this.label19.TabIndex = 75;
            this.label19.Text = "Definition:";
            // 
            // cb_definition
            // 
            this.cb_definition.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.cb_definition.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cb_definition.FormattingEnabled = true;
            this.cb_definition.Location = new System.Drawing.Point(268, 65);
            this.cb_definition.Margin = new System.Windows.Forms.Padding(4);
            this.cb_definition.Name = "cb_definition";
            this.cb_definition.Size = new System.Drawing.Size(205, 24);
            this.cb_definition.TabIndex = 74;
            this.cb_definition.SelectedIndexChanged += new System.EventHandler(this.cb_definition_SelectedIndexChanged);
            // 
            // textBox_NAy_Input
            // 
            this.textBox_NAy_Input.Location = new System.Drawing.Point(617, 113);
            this.textBox_NAy_Input.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.textBox_NAy_Input.Name = "textBox_NAy_Input";
            this.textBox_NAy_Input.Size = new System.Drawing.Size(116, 22);
            this.textBox_NAy_Input.TabIndex = 2;
            this.textBox_NAy_Input.TextChanged += new System.EventHandler(this.textBox4_TextChanged);
            // 
            // Definition_y
            // 
            this.Definition_y.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.Definition_y.AutoSize = true;
            this.Definition_y.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Definition_y.Location = new System.Drawing.Point(404, 114);
            this.Definition_y.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.Definition_y.Name = "Definition_y";
            this.Definition_y.Size = new System.Drawing.Size(103, 21);
            this.Definition_y.TabIndex = 47;
            this.Definition_y.Text = "NAy (1/e^2):";
            this.Definition_y.Click += new System.EventHandler(this.label15_Click);
            // 
            // textBox_NAx_Input
            // 
            this.textBox_NAx_Input.Location = new System.Drawing.Point(268, 114);
            this.textBox_NAx_Input.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.textBox_NAx_Input.Name = "textBox_NAx_Input";
            this.textBox_NAx_Input.Size = new System.Drawing.Size(116, 22);
            this.textBox_NAx_Input.TabIndex = 1;
            this.textBox_NAx_Input.TextChanged += new System.EventHandler(this.textBox2_TextChanged);
            // 
            // Definition_x
            // 
            this.Definition_x.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.Definition_x.AutoSize = true;
            this.Definition_x.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Definition_x.Location = new System.Drawing.Point(16, 114);
            this.Definition_x.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.Definition_x.Name = "Definition_x";
            this.Definition_x.Size = new System.Drawing.Size(105, 21);
            this.Definition_x.TabIndex = 41;
            this.Definition_x.Text = "NAx (1/e^2):";
            this.Definition_x.Click += new System.EventHandler(this.label12_Click);
            // 
            // label11
            // 
            this.label11.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label11.AutoSize = true;
            this.label11.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label11.Location = new System.Drawing.Point(16, 25);
            this.label11.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(141, 21);
            this.label11.TabIndex = 38;
            this.label11.Text = "Wavelength (µm):";
            this.label11.Click += new System.EventHandler(this.label11_Click);
            // 
            // cb_WaveNum
            // 
            this.cb_WaveNum.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.cb_WaveNum.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cb_WaveNum.FormattingEnabled = true;
            this.cb_WaveNum.Location = new System.Drawing.Point(268, 20);
            this.cb_WaveNum.Margin = new System.Windows.Forms.Padding(4);
            this.cb_WaveNum.Name = "cb_WaveNum";
            this.cb_WaveNum.Size = new System.Drawing.Size(117, 24);
            this.cb_WaveNum.TabIndex = 0;
            this.cb_WaveNum.SelectedIndexChanged += new System.EventHandler(this.comboBox1_SelectedIndexChanged);
            // 
            // tabPage3
            // 
            this.tabPage3.Controls.Add(this.button4);
            this.tabPage3.Controls.Add(this.groupBox6);
            this.tabPage3.Controls.Add(this.groupBox5);
            this.tabPage3.Controls.Add(this.groupBox4);
            this.tabPage3.Location = new System.Drawing.Point(4, 25);
            this.tabPage3.Margin = new System.Windows.Forms.Padding(4);
            this.tabPage3.Name = "tabPage3";
            this.tabPage3.Padding = new System.Windows.Forms.Padding(4);
            this.tabPage3.Size = new System.Drawing.Size(799, 488);
            this.tabPage3.TabIndex = 2;
            this.tabPage3.Text = "Check";
            this.tabPage3.UseVisualStyleBackColor = true;
            // 
            // button4
            // 
            this.button4.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button4.Location = new System.Drawing.Point(312, 422);
            this.button4.Margin = new System.Windows.Forms.Padding(4);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(189, 47);
            this.button4.TabIndex = 6;
            this.button4.Text = "Calculate!";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click_1);
            // 
            // groupBox6
            // 
            this.groupBox6.Controls.Add(this.label_WaistY_Check);
            this.groupBox6.Controls.Add(this.label_WaistX_Check);
            this.groupBox6.Controls.Add(this.label23);
            this.groupBox6.Controls.Add(this.label24);
            this.groupBox6.Controls.Add(this.label_AngleY_Check);
            this.groupBox6.Controls.Add(this.label_AngleX_Check);
            this.groupBox6.Controls.Add(this.label10);
            this.groupBox6.Controls.Add(this.label18);
            this.groupBox6.Location = new System.Drawing.Point(19, 308);
            this.groupBox6.Margin = new System.Windows.Forms.Padding(4);
            this.groupBox6.Name = "groupBox6";
            this.groupBox6.Padding = new System.Windows.Forms.Padding(4);
            this.groupBox6.Size = new System.Drawing.Size(743, 107);
            this.groupBox6.TabIndex = 78;
            this.groupBox6.TabStop = false;
            this.groupBox6.Text = "POP";
            // 
            // label_WaistY_Check
            // 
            this.label_WaistY_Check.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_WaistY_Check.AutoSize = true;
            this.label_WaistY_Check.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_WaistY_Check.Location = new System.Drawing.Point(645, 62);
            this.label_WaistY_Check.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_WaistY_Check.Name = "label_WaistY_Check";
            this.label_WaistY_Check.Size = new System.Drawing.Size(33, 21);
            this.label_WaistY_Check.TabIndex = 75;
            this.label_WaistY_Check.Text = "0.0";
            // 
            // label_WaistX_Check
            // 
            this.label_WaistX_Check.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_WaistX_Check.AutoSize = true;
            this.label_WaistX_Check.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_WaistX_Check.Location = new System.Drawing.Point(255, 62);
            this.label_WaistX_Check.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_WaistX_Check.Name = "label_WaistX_Check";
            this.label_WaistX_Check.Size = new System.Drawing.Size(33, 21);
            this.label_WaistX_Check.TabIndex = 74;
            this.label_WaistX_Check.Text = "0.0";
            // 
            // label23
            // 
            this.label23.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label23.AutoSize = true;
            this.label23.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label23.Location = new System.Drawing.Point(383, 62);
            this.label23.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label23.Name = "label23";
            this.label23.Size = new System.Drawing.Size(171, 21);
            this.label23.TabIndex = 73;
            this.label23.Text = "WaistY (1/e^2) in µm:";
            // 
            // label24
            // 
            this.label24.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label24.AutoSize = true;
            this.label24.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label24.Location = new System.Drawing.Point(5, 62);
            this.label24.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label24.Name = "label24";
            this.label24.Size = new System.Drawing.Size(177, 21);
            this.label24.TabIndex = 72;
            this.label24.Text = "WaistX (1/e^2) in µm :";
            // 
            // label_AngleY_Check
            // 
            this.label_AngleY_Check.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_AngleY_Check.AutoSize = true;
            this.label_AngleY_Check.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_AngleY_Check.Location = new System.Drawing.Point(645, 32);
            this.label_AngleY_Check.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_AngleY_Check.Name = "label_AngleY_Check";
            this.label_AngleY_Check.Size = new System.Drawing.Size(33, 21);
            this.label_AngleY_Check.TabIndex = 71;
            this.label_AngleY_Check.Text = "0.0";
            // 
            // label_AngleX_Check
            // 
            this.label_AngleX_Check.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_AngleX_Check.AutoSize = true;
            this.label_AngleX_Check.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_AngleX_Check.Location = new System.Drawing.Point(255, 32);
            this.label_AngleX_Check.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_AngleX_Check.Name = "label_AngleX_Check";
            this.label_AngleX_Check.Size = new System.Drawing.Size(33, 21);
            this.label_AngleX_Check.TabIndex = 70;
            this.label_AngleX_Check.Text = "0.0";
            // 
            // label10
            // 
            this.label10.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label10.AutoSize = true;
            this.label10.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label10.Location = new System.Drawing.Point(380, 32);
            this.label10.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(171, 21);
            this.label10.TabIndex = 68;
            this.label10.Text = "AngleY(1/e^2) in deg:";
            // 
            // label18
            // 
            this.label18.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label18.AutoSize = true;
            this.label18.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label18.Location = new System.Drawing.Point(5, 32);
            this.label18.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label18.Name = "label18";
            this.label18.Size = new System.Drawing.Size(171, 21);
            this.label18.TabIndex = 67;
            this.label18.Text = "AngleX(1/e^2) in deg:";
            this.label18.Click += new System.EventHandler(this.label18_Click_1);
            // 
            // groupBox5
            // 
            this.groupBox5.Controls.Add(this.label_NAX_Check);
            this.groupBox5.Controls.Add(this.label_NAY_Check);
            this.groupBox5.Controls.Add(this.label33);
            this.groupBox5.Controls.Add(this.label21);
            this.groupBox5.Location = new System.Drawing.Point(17, 206);
            this.groupBox5.Margin = new System.Windows.Forms.Padding(4);
            this.groupBox5.Name = "groupBox5";
            this.groupBox5.Padding = new System.Windows.Forms.Padding(4);
            this.groupBox5.Size = new System.Drawing.Size(741, 95);
            this.groupBox5.TabIndex = 77;
            this.groupBox5.TabStop = false;
            this.groupBox5.Text = "Fiber Coupling";
            // 
            // label_NAX_Check
            // 
            this.label_NAX_Check.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_NAX_Check.AutoSize = true;
            this.label_NAX_Check.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_NAX_Check.Location = new System.Drawing.Point(208, 48);
            this.label_NAX_Check.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_NAX_Check.Name = "label_NAX_Check";
            this.label_NAX_Check.Size = new System.Drawing.Size(33, 21);
            this.label_NAX_Check.TabIndex = 61;
            this.label_NAX_Check.Text = "0.0";
            // 
            // label_NAY_Check
            // 
            this.label_NAY_Check.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label_NAY_Check.AutoSize = true;
            this.label_NAY_Check.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_NAY_Check.Location = new System.Drawing.Point(647, 48);
            this.label_NAY_Check.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label_NAY_Check.Name = "label_NAY_Check";
            this.label_NAY_Check.Size = new System.Drawing.Size(33, 21);
            this.label_NAY_Check.TabIndex = 59;
            this.label_NAY_Check.Text = "0.0";
            // 
            // label33
            // 
            this.label33.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label33.AutoSize = true;
            this.label33.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label33.Location = new System.Drawing.Point(381, 48);
            this.label33.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label33.Name = "label33";
            this.label33.Size = new System.Drawing.Size(103, 21);
            this.label33.TabIndex = 47;
            this.label33.Text = "NAy (1/e^2):";
            // 
            // label21
            // 
            this.label21.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label21.AutoSize = true;
            this.label21.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label21.Location = new System.Drawing.Point(4, 48);
            this.label21.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label21.Name = "label21";
            this.label21.Size = new System.Drawing.Size(105, 21);
            this.label21.TabIndex = 41;
            this.label21.Text = "NAx (1/e^2):";
            // 
            // groupBox4
            // 
            this.groupBox4.Controls.Add(this.label30);
            this.groupBox4.Controls.Add(this.label31);
            this.groupBox4.Controls.Add(this.textBox_VCY_Check);
            this.groupBox4.Controls.Add(this.textBox_G_Check);
            this.groupBox4.Controls.Add(this.label34);
            this.groupBox4.Controls.Add(this.textBox_VCX_Check);
            this.groupBox4.Controls.Add(this.textBox_NA_Check);
            this.groupBox4.Controls.Add(this.label37);
            this.groupBox4.Controls.Add(this.label22);
            this.groupBox4.Controls.Add(this.cb_WaveNum2);
            this.groupBox4.Location = new System.Drawing.Point(15, 12);
            this.groupBox4.Margin = new System.Windows.Forms.Padding(4);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Padding = new System.Windows.Forms.Padding(4);
            this.groupBox4.Size = new System.Drawing.Size(747, 176);
            this.groupBox4.TabIndex = 76;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "System Explorer";
            // 
            // label30
            // 
            this.label30.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label30.AutoSize = true;
            this.label30.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label30.Location = new System.Drawing.Point(8, 79);
            this.label30.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label30.Name = "label30";
            this.label30.Size = new System.Drawing.Size(146, 21);
            this.label30.TabIndex = 54;
            this.label30.Text = "Object Space NA:";
            // 
            // label31
            // 
            this.label31.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label31.AutoSize = true;
            this.label31.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label31.Location = new System.Drawing.Point(383, 130);
            this.label31.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label31.Name = "label31";
            this.label31.Size = new System.Drawing.Size(184, 21);
            this.label31.TabIndex = 50;
            this.label31.Text = "Vignetting Factor VCY:";
            // 
            // textBox_VCY_Check
            // 
            this.textBox_VCY_Check.Location = new System.Drawing.Point(609, 130);
            this.textBox_VCY_Check.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.textBox_VCY_Check.Name = "textBox_VCY_Check";
            this.textBox_VCY_Check.Size = new System.Drawing.Size(116, 22);
            this.textBox_VCY_Check.TabIndex = 4;
            this.textBox_VCY_Check.TextChanged += new System.EventHandler(this.textBox_VCY_Check_TextChanged);
            // 
            // textBox_G_Check
            // 
            this.textBox_G_Check.Location = new System.Drawing.Point(609, 78);
            this.textBox_G_Check.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.textBox_G_Check.Name = "textBox_G_Check";
            this.textBox_G_Check.Size = new System.Drawing.Size(116, 22);
            this.textBox_G_Check.TabIndex = 2;
            // 
            // label34
            // 
            this.label34.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label34.AutoSize = true;
            this.label34.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label34.Location = new System.Drawing.Point(9, 130);
            this.label34.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label34.Name = "label34";
            this.label34.Size = new System.Drawing.Size(186, 21);
            this.label34.TabIndex = 45;
            this.label34.Text = "Vignetting Factor VCX:";
            // 
            // textBox_VCX_Check
            // 
            this.textBox_VCX_Check.Location = new System.Drawing.Point(216, 130);
            this.textBox_VCX_Check.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.textBox_VCX_Check.Name = "textBox_VCX_Check";
            this.textBox_VCX_Check.Size = new System.Drawing.Size(116, 22);
            this.textBox_VCX_Check.TabIndex = 3;
            this.textBox_VCX_Check.TextChanged += new System.EventHandler(this.textBox7_TextChanged);
            // 
            // textBox_NA_Check
            // 
            this.textBox_NA_Check.Location = new System.Drawing.Point(216, 81);
            this.textBox_NA_Check.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.textBox_NA_Check.Name = "textBox_NA_Check";
            this.textBox_NA_Check.Size = new System.Drawing.Size(116, 22);
            this.textBox_NA_Check.TabIndex = 1;
            // 
            // label37
            // 
            this.label37.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label37.AutoSize = true;
            this.label37.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label37.Location = new System.Drawing.Point(384, 82);
            this.label37.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label37.Name = "label37";
            this.label37.Size = new System.Drawing.Size(190, 21);
            this.label37.TabIndex = 43;
            this.label37.Text = "Apodization Factor (G):";
            // 
            // label22
            // 
            this.label22.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.label22.AutoSize = true;
            this.label22.Font = new System.Drawing.Font("Times New Roman", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label22.Location = new System.Drawing.Point(9, 37);
            this.label22.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label22.Name = "label22";
            this.label22.Size = new System.Drawing.Size(99, 21);
            this.label22.TabIndex = 38;
            this.label22.Text = "Wavelength:";
            this.label22.Click += new System.EventHandler(this.label22_Click);
            // 
            // cb_WaveNum2
            // 
            this.cb_WaveNum2.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.cb_WaveNum2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cb_WaveNum2.FormattingEnabled = true;
            this.cb_WaveNum2.Location = new System.Drawing.Point(216, 32);
            this.cb_WaveNum2.Margin = new System.Windows.Forms.Padding(4);
            this.cb_WaveNum2.Name = "cb_WaveNum2";
            this.cb_WaveNum2.Size = new System.Drawing.Size(117, 24);
            this.cb_WaveNum2.TabIndex = 0;
            this.cb_WaveNum2.SelectedIndexChanged += new System.EventHandler(this.cb_WaveNum2_SelectedIndexChanged);
            // 
            // ExtensionSettingsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(805, 518);
            this.Controls.Add(this.Input);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Margin = new System.Windows.Forms.Padding(4);
            this.MinimumSize = new System.Drawing.Size(598, 246);
            this.Name = "ExtensionSettingsForm";
            this.Text = "Calculator for Fiber / Laser";
            this.Load += new System.EventHandler(this.ExtensionSettingsForm_Load_1);
            ((System.ComponentModel.ISupportInitialize)(this.fileSystemWatcher1)).EndInit();
            this.Input.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.tabPage3.ResumeLayout(false);
            this.groupBox6.ResumeLayout(false);
            this.groupBox6.PerformLayout();
            this.groupBox5.ResumeLayout(false);
            this.groupBox5.PerformLayout();
            this.groupBox4.ResumeLayout(false);
            this.groupBox4.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.IO.FileSystemWatcher fileSystemWatcher1;
        private System.Windows.Forms.TabControl Input;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.Label label_ObjectNA_Input;
        private System.Windows.Forms.Label label_VCX_Input;
        private System.Windows.Forms.Label label17;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.TextBox textBox_NAy_Input;
        private System.Windows.Forms.Label Definition_y;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.TextBox textBox_G_Input;
        private System.Windows.Forms.TextBox textBox_NAx_Input;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Label Definition_x;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.ComboBox cb_WaveNum;
        private System.Windows.Forms.TabPage tabPage3;
        private System.Windows.Forms.Label label_NAX_Check;
        private System.Windows.Forms.Label label_NAY_Check;
        private System.Windows.Forms.Label label30;
        private System.Windows.Forms.Label label31;
        private System.Windows.Forms.TextBox textBox_VCY_Check;
        private System.Windows.Forms.Label label33;
        private System.Windows.Forms.TextBox textBox_G_Check;
        private System.Windows.Forms.Label label34;
        private System.Windows.Forms.TextBox textBox_VCX_Check;
        private System.Windows.Forms.TextBox textBox_NA_Check;
        private System.Windows.Forms.Label label37;
        private System.Windows.Forms.Label label21;
        private System.Windows.Forms.Label label22;
        private System.Windows.Forms.ComboBox cb_WaveNum2;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label_AngleX_Input;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label_WaistY_Input;
        private System.Windows.Forms.Label label_WaistX_Input;
        private System.Windows.Forms.Label label_AngleY_Input;
        private System.Windows.Forms.Label label_VCY_Input;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label_Intensity_Input;
        private System.Windows.Forms.Label label_AngleY_Check;
        private System.Windows.Forms.Label label_AngleX_Check;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Label label18;
        private System.Windows.Forms.Label label_WaistY_Check;
        private System.Windows.Forms.Label label_WaistX_Check;
        private System.Windows.Forms.Label label23;
        private System.Windows.Forms.Label label24;
        private System.Windows.Forms.Label label19;
        private System.Windows.Forms.ComboBox cb_definition;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox6;
        private System.Windows.Forms.GroupBox groupBox5;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Button button4;
    }
}