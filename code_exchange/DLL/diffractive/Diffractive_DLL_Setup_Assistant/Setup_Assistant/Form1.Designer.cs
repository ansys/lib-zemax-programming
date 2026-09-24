namespace Diffractive_DLL_Setup_Assistant
{
    partial class Form1
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
            this.label1 = new System.Windows.Forms.Label();
            this.b_loadvalue = new System.Windows.Forms.Button();
            this.b_loadpar = new System.Windows.Forms.Button();
            this.b_setMCE = new System.Windows.Forms.Button();
            this.tb_single_obj = new System.Windows.Forms.TextBox();
            this.tb_parameters = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.tb_values = new System.Windows.Forms.TextBox();
            this.b_set_parameter = new System.Windows.Forms.Button();
            this.tb_objects = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.chk_set_trans = new System.Windows.Forms.CheckBox();
            this.b_detect_obj = new System.Windows.Forms.Button();
            this.b_copy_par = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            this.b_LinkOn = new System.Windows.Forms.Button();
            this.b_LinkOff = new System.Windows.Forms.Button();
            this.b_LinkOn99 = new System.Windows.Forms.Button();
            this.gb_step1 = new System.Windows.Forms.GroupBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.gb_step1.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(52, 48);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(74, 20);
            this.label1.TabIndex = 0;
            this.label1.Text = "From Obj";
            // 
            // b_loadvalue
            // 
            this.b_loadvalue.Location = new System.Drawing.Point(681, 138);
            this.b_loadvalue.Name = "b_loadvalue";
            this.b_loadvalue.Size = new System.Drawing.Size(128, 42);
            this.b_loadvalue.TabIndex = 4;
            this.b_loadvalue.Text = "Load Values";
            this.b_loadvalue.UseVisualStyleBackColor = true;
            this.b_loadvalue.Click += new System.EventHandler(this.b_loadvalue_Click);
            // 
            // b_loadpar
            // 
            this.b_loadpar.Location = new System.Drawing.Point(681, 90);
            this.b_loadpar.Name = "b_loadpar";
            this.b_loadpar.Size = new System.Drawing.Size(128, 42);
            this.b_loadpar.TabIndex = 2;
            this.b_loadpar.Text = "Load Par#";
            this.b_loadpar.UseVisualStyleBackColor = true;
            this.b_loadpar.Click += new System.EventHandler(this.b_loadpar_Click);
            // 
            // b_setMCE
            // 
            this.b_setMCE.Location = new System.Drawing.Point(33, 48);
            this.b_setMCE.Name = "b_setMCE";
            this.b_setMCE.Size = new System.Drawing.Size(101, 42);
            this.b_setMCE.TabIndex = 7;
            this.b_setMCE.Text = "Set MCE";
            this.b_setMCE.UseVisualStyleBackColor = true;
            this.b_setMCE.Click += new System.EventHandler(this.b_setMCE_Click);
            // 
            // tb_single_obj
            // 
            this.tb_single_obj.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tb_single_obj.Location = new System.Drawing.Point(132, 38);
            this.tb_single_obj.Name = "tb_single_obj";
            this.tb_single_obj.Size = new System.Drawing.Size(62, 35);
            this.tb_single_obj.TabIndex = 0;
            // 
            // tb_parameters
            // 
            this.tb_parameters.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tb_parameters.Location = new System.Drawing.Point(132, 94);
            this.tb_parameters.Name = "tb_parameters";
            this.tb_parameters.Size = new System.Drawing.Size(543, 35);
            this.tb_parameters.TabIndex = 1;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(84, 101);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(42, 20);
            this.label2.TabIndex = 8;
            this.label2.Text = "Par#";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(66, 149);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(60, 20);
            this.label3.TabIndex = 9;
            this.label3.Text = "Par Val";
            // 
            // tb_values
            // 
            this.tb_values.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tb_values.Location = new System.Drawing.Point(132, 142);
            this.tb_values.Name = "tb_values";
            this.tb_values.Size = new System.Drawing.Size(543, 35);
            this.tb_values.TabIndex = 3;
            // 
            // b_set_parameter
            // 
            this.b_set_parameter.Location = new System.Drawing.Point(153, 48);
            this.b_set_parameter.Name = "b_set_parameter";
            this.b_set_parameter.Size = new System.Drawing.Size(143, 42);
            this.b_set_parameter.TabIndex = 8;
            this.b_set_parameter.Text = "Set parameters";
            this.b_set_parameter.UseVisualStyleBackColor = true;
            this.b_set_parameter.Click += new System.EventHandler(this.b_set_parameter_Click);
            // 
            // tb_objects
            // 
            this.tb_objects.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tb_objects.Location = new System.Drawing.Point(132, 190);
            this.tb_objects.Name = "tb_objects";
            this.tb_objects.Size = new System.Drawing.Size(543, 35);
            this.tb_objects.TabIndex = 5;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(63, 197);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(63, 20);
            this.label5.TabIndex = 17;
            this.label5.Text = "To Objs";
            // 
            // chk_set_trans
            // 
            this.chk_set_trans.AutoSize = true;
            this.chk_set_trans.Location = new System.Drawing.Point(33, 114);
            this.chk_set_trans.Name = "chk_set_trans";
            this.chk_set_trans.Size = new System.Drawing.Size(192, 24);
            this.chk_set_trans.TabIndex = 9;
            this.chk_set_trans.Text = "Also Set Transmission";
            this.chk_set_trans.UseVisualStyleBackColor = true;
            // 
            // b_detect_obj
            // 
            this.b_detect_obj.Location = new System.Drawing.Point(681, 186);
            this.b_detect_obj.Name = "b_detect_obj";
            this.b_detect_obj.Size = new System.Drawing.Size(128, 42);
            this.b_detect_obj.TabIndex = 6;
            this.b_detect_obj.Text = "Auto Detect";
            this.b_detect_obj.UseVisualStyleBackColor = true;
            this.b_detect_obj.Click += new System.EventHandler(this.b_detect_obj_Click);
            // 
            // b_copy_par
            // 
            this.b_copy_par.Location = new System.Drawing.Point(312, 48);
            this.b_copy_par.Name = "b_copy_par";
            this.b_copy_par.Size = new System.Drawing.Size(153, 42);
            this.b_copy_par.TabIndex = 18;
            this.b_copy_par.Text = "Copy parameters";
            this.b_copy_par.UseVisualStyleBackColor = true;
            this.b_copy_par.Click += new System.EventHandler(this.b_copy_par_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(892, 35);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(98, 20);
            this.label4.TabIndex = 19;
            this.label4.Text = "-- Shortcut --";
            // 
            // b_LinkOn
            // 
            this.b_LinkOn.Location = new System.Drawing.Point(877, 66);
            this.b_LinkOn.Name = "b_LinkOn";
            this.b_LinkOn.Size = new System.Drawing.Size(156, 42);
            this.b_LinkOn.TabIndex = 20;
            this.b_LinkOn.Text = "Link Lum On (1)";
            this.b_LinkOn.UseVisualStyleBackColor = true;
            this.b_LinkOn.Click += new System.EventHandler(this.b_LinkOn_Click);
            // 
            // b_LinkOff
            // 
            this.b_LinkOff.Location = new System.Drawing.Point(877, 165);
            this.b_LinkOff.Name = "b_LinkOff";
            this.b_LinkOff.Size = new System.Drawing.Size(156, 42);
            this.b_LinkOff.TabIndex = 21;
            this.b_LinkOff.Text = "Link Lum Off";
            this.b_LinkOff.UseVisualStyleBackColor = true;
            this.b_LinkOff.Click += new System.EventHandler(this.b_LinkOff_Click);
            // 
            // b_LinkOn99
            // 
            this.b_LinkOn99.Location = new System.Drawing.Point(877, 117);
            this.b_LinkOn99.Name = "b_LinkOn99";
            this.b_LinkOn99.Size = new System.Drawing.Size(156, 42);
            this.b_LinkOn99.TabIndex = 22;
            this.b_LinkOn99.Text = "Link Lum On (99)";
            this.b_LinkOn99.UseVisualStyleBackColor = true;
            this.b_LinkOn99.Click += new System.EventHandler(this.b_LinkOn99_Click);
            // 
            // gb_step1
            // 
            this.gb_step1.Controls.Add(this.label1);
            this.gb_step1.Controls.Add(this.b_LinkOn99);
            this.gb_step1.Controls.Add(this.b_loadvalue);
            this.gb_step1.Controls.Add(this.b_LinkOff);
            this.gb_step1.Controls.Add(this.b_loadpar);
            this.gb_step1.Controls.Add(this.b_LinkOn);
            this.gb_step1.Controls.Add(this.tb_single_obj);
            this.gb_step1.Controls.Add(this.label4);
            this.gb_step1.Controls.Add(this.tb_parameters);
            this.gb_step1.Controls.Add(this.label2);
            this.gb_step1.Controls.Add(this.b_detect_obj);
            this.gb_step1.Controls.Add(this.label3);
            this.gb_step1.Controls.Add(this.tb_values);
            this.gb_step1.Controls.Add(this.label5);
            this.gb_step1.Controls.Add(this.tb_objects);
            this.gb_step1.Location = new System.Drawing.Point(28, 27);
            this.gb_step1.Name = "gb_step1";
            this.gb_step1.Size = new System.Drawing.Size(1075, 261);
            this.gb_step1.TabIndex = 23;
            this.gb_step1.TabStop = false;
            this.gb_step1.Text = "Step 1 - Settings";
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.b_setMCE);
            this.groupBox1.Controls.Add(this.b_set_parameter);
            this.groupBox1.Controls.Add(this.b_copy_par);
            this.groupBox1.Controls.Add(this.chk_set_trans);
            this.groupBox1.Location = new System.Drawing.Point(28, 334);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(579, 160);
            this.groupBox1.TabIndex = 24;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Step 2 - Change System";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1146, 523);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.gb_step1);
            this.Name = "Form1";
            this.Text = "Diffractive DLL Setup Assistant";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.Load += new System.EventHandler(this.Form1_Load);
            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.Form1_KeyDown);
            this.gb_step1.ResumeLayout(false);
            this.gb_step1.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button b_loadvalue;
        private System.Windows.Forms.Button b_loadpar;
        private System.Windows.Forms.Button b_setMCE;
        private System.Windows.Forms.TextBox tb_single_obj;
        private System.Windows.Forms.TextBox tb_parameters;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox tb_values;
        private System.Windows.Forms.Button b_set_parameter;
        private System.Windows.Forms.TextBox tb_objects;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.CheckBox chk_set_trans;
        private System.Windows.Forms.Button b_detect_obj;
        private System.Windows.Forms.Button b_copy_par;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button b_LinkOn;
        private System.Windows.Forms.Button b_LinkOff;
        private System.Windows.Forms.Button b_LinkOn99;
        private System.Windows.Forms.GroupBox gb_step1;
        private System.Windows.Forms.GroupBox groupBox1;
    }
}