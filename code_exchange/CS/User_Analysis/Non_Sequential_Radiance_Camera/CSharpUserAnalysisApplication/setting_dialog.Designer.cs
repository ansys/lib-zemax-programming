
namespace RadianceCamera
{
    partial class setting_dialog
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
            this.lab_xwidth = new System.Windows.Forms.Label();
            this.lab_ywidth = new System.Windows.Forms.Label();
            this.lab_ypix = new System.Windows.Forms.Label();
            this.lab_xpix = new System.Windows.Forms.Label();
            this.tb_xwid = new System.Windows.Forms.TextBox();
            this.tb_ywid = new System.Windows.Forms.TextBox();
            this.tb_xpix = new System.Windows.Forms.TextBox();
            this.tb_ypix = new System.Windows.Forms.TextBox();
            this.tb_targetz = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.bt_load = new System.Windows.Forms.Button();
            this.tb_objnum = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.tb_sourcpath = new System.Windows.Forms.TextBox();
            this.bt_OK = new System.Windows.Forms.Button();
            this.bt_applybt_apply = new System.Windows.Forms.Button();
            this.bt_cancel = new System.Windows.Forms.Button();
            this.tb_wavnum = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.chk_islog = new System.Windows.Forms.CheckBox();
            this.chk_PSA = new System.Windows.Forms.CheckBox();
            this.tb_smooth = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.bt_tip = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // lab_xwidth
            // 
            this.lab_xwidth.AutoSize = true;
            this.lab_xwidth.Location = new System.Drawing.Point(22, 53);
            this.lab_xwidth.Name = "lab_xwidth";
            this.lab_xwidth.Size = new System.Drawing.Size(45, 12);
            this.lab_xwidth.TabIndex = 0;
            this.lab_xwidth.Text = "X Width";
            // 
            // lab_ywidth
            // 
            this.lab_ywidth.AutoSize = true;
            this.lab_ywidth.Location = new System.Drawing.Point(22, 83);
            this.lab_ywidth.Name = "lab_ywidth";
            this.lab_ywidth.Size = new System.Drawing.Size(45, 12);
            this.lab_ywidth.TabIndex = 1;
            this.lab_ywidth.Text = "Y Width";
            // 
            // lab_ypix
            // 
            this.lab_ypix.AutoSize = true;
            this.lab_ypix.Location = new System.Drawing.Point(22, 143);
            this.lab_ypix.Name = "lab_ypix";
            this.lab_ypix.Size = new System.Drawing.Size(39, 12);
            this.lab_ypix.TabIndex = 3;
            this.lab_ypix.Text = "Y Pixel";
            // 
            // lab_xpix
            // 
            this.lab_xpix.AutoSize = true;
            this.lab_xpix.Location = new System.Drawing.Point(22, 113);
            this.lab_xpix.Name = "lab_xpix";
            this.lab_xpix.Size = new System.Drawing.Size(39, 12);
            this.lab_xpix.TabIndex = 2;
            this.lab_xpix.Text = "X Pixel";
            // 
            // tb_xwid
            // 
            this.tb_xwid.Location = new System.Drawing.Point(114, 48);
            this.tb_xwid.Name = "tb_xwid";
            this.tb_xwid.Size = new System.Drawing.Size(59, 22);
            this.tb_xwid.TabIndex = 1;
            this.tb_xwid.Text = "1";
            this.tb_xwid.Validating += new System.ComponentModel.CancelEventHandler(this.tb_xwid_Validating);
            // 
            // tb_ywid
            // 
            this.tb_ywid.Location = new System.Drawing.Point(114, 78);
            this.tb_ywid.Name = "tb_ywid";
            this.tb_ywid.Size = new System.Drawing.Size(59, 22);
            this.tb_ywid.TabIndex = 2;
            this.tb_ywid.Text = "1";
            this.tb_ywid.Validating += new System.ComponentModel.CancelEventHandler(this.tb_ywid_Validating);
            // 
            // tb_xpix
            // 
            this.tb_xpix.Location = new System.Drawing.Point(114, 108);
            this.tb_xpix.Name = "tb_xpix";
            this.tb_xpix.Size = new System.Drawing.Size(59, 22);
            this.tb_xpix.TabIndex = 3;
            this.tb_xpix.Text = "100";
            this.tb_xpix.Validating += new System.ComponentModel.CancelEventHandler(this.tb_xpix_Validating);
            // 
            // tb_ypix
            // 
            this.tb_ypix.Location = new System.Drawing.Point(114, 138);
            this.tb_ypix.Name = "tb_ypix";
            this.tb_ypix.Size = new System.Drawing.Size(59, 22);
            this.tb_ypix.TabIndex = 4;
            this.tb_ypix.Text = "100";
            this.tb_ypix.Validating += new System.ComponentModel.CancelEventHandler(this.tb_ypix_Validating);
            // 
            // tb_targetz
            // 
            this.tb_targetz.Location = new System.Drawing.Point(114, 168);
            this.tb_targetz.Name = "tb_targetz";
            this.tb_targetz.Size = new System.Drawing.Size(59, 22);
            this.tb_targetz.TabIndex = 5;
            this.tb_targetz.Text = "100";
            this.tb_targetz.Validating += new System.ComponentModel.CancelEventHandler(this.tb_targetz_Validating);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(22, 173);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(45, 12);
            this.label1.TabIndex = 8;
            this.label1.Text = "Target Z";
            // 
            // bt_load
            // 
            this.bt_load.Location = new System.Drawing.Point(24, 293);
            this.bt_load.Name = "bt_load";
            this.bt_load.Size = new System.Drawing.Size(149, 25);
            this.bt_load.TabIndex = 6;
            this.bt_load.Text = "Select Source (.dat or .sdf)";
            this.bt_load.UseVisualStyleBackColor = true;
            this.bt_load.Click += new System.EventHandler(this.bt_load_Click);
            // 
            // tb_objnum
            // 
            this.tb_objnum.Location = new System.Drawing.Point(114, 18);
            this.tb_objnum.Name = "tb_objnum";
            this.tb_objnum.Size = new System.Drawing.Size(59, 22);
            this.tb_objnum.TabIndex = 0;
            this.tb_objnum.Text = "1";
            this.tb_objnum.Validating += new System.ComponentModel.CancelEventHandler(this.tb_objnum_Validating);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(22, 23);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(70, 12);
            this.label2.TabIndex = 11;
            this.label2.Text = "Annulus Obj#";
            // 
            // tb_sourcpath
            // 
            this.tb_sourcpath.Location = new System.Drawing.Point(24, 324);
            this.tb_sourcpath.Multiline = true;
            this.tb_sourcpath.Name = "tb_sourcpath";
            this.tb_sourcpath.ReadOnly = true;
            this.tb_sourcpath.Size = new System.Drawing.Size(149, 81);
            this.tb_sourcpath.TabIndex = 12;
            // 
            // bt_OK
            // 
            this.bt_OK.Location = new System.Drawing.Point(24, 411);
            this.bt_OK.Name = "bt_OK";
            this.bt_OK.Size = new System.Drawing.Size(37, 25);
            this.bt_OK.TabIndex = 13;
            this.bt_OK.Text = "OK";
            this.bt_OK.UseVisualStyleBackColor = true;
            this.bt_OK.Click += new System.EventHandler(this.bt_OK_Click);
            // 
            // bt_applybt_apply
            // 
            this.bt_applybt_apply.Location = new System.Drawing.Point(68, 411);
            this.bt_applybt_apply.Name = "bt_applybt_apply";
            this.bt_applybt_apply.Size = new System.Drawing.Size(51, 25);
            this.bt_applybt_apply.TabIndex = 14;
            this.bt_applybt_apply.Text = "Apply";
            this.bt_applybt_apply.UseVisualStyleBackColor = true;
            this.bt_applybt_apply.Click += new System.EventHandler(this.bt_applybt_apply_Click);
            // 
            // bt_cancel
            // 
            this.bt_cancel.Location = new System.Drawing.Point(125, 411);
            this.bt_cancel.Name = "bt_cancel";
            this.bt_cancel.Size = new System.Drawing.Size(48, 25);
            this.bt_cancel.TabIndex = 15;
            this.bt_cancel.Text = "Cancel";
            this.bt_cancel.UseVisualStyleBackColor = true;
            this.bt_cancel.Click += new System.EventHandler(this.bt_cancel_Click);
            // 
            // tb_wavnum
            // 
            this.tb_wavnum.Location = new System.Drawing.Point(114, 197);
            this.tb_wavnum.Name = "tb_wavnum";
            this.tb_wavnum.Size = new System.Drawing.Size(59, 22);
            this.tb_wavnum.TabIndex = 16;
            this.tb_wavnum.Text = "0";
            this.tb_wavnum.Validating += new System.ComponentModel.CancelEventHandler(this.tb_wavnum_Validating);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(22, 202);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(41, 12);
            this.label3.TabIndex = 17;
            this.label3.Text = "Wave #";
            // 
            // chk_islog
            // 
            this.chk_islog.AutoSize = true;
            this.chk_islog.Location = new System.Drawing.Point(24, 264);
            this.chk_islog.Name = "chk_islog";
            this.chk_islog.Size = new System.Drawing.Size(43, 16);
            this.chk_islog.TabIndex = 19;
            this.chk_islog.Text = "Log";
            this.chk_islog.UseVisualStyleBackColor = true;
            // 
            // chk_PSA
            // 
            this.chk_PSA.AutoSize = true;
            this.chk_PSA.Location = new System.Drawing.Point(100, 262);
            this.chk_PSA.Name = "chk_PSA";
            this.chk_PSA.Size = new System.Drawing.Size(71, 16);
            this.chk_PSA.TabIndex = 20;
            this.chk_PSA.Text = "Irradiance";
            this.chk_PSA.UseVisualStyleBackColor = true;
            // 
            // tb_smooth
            // 
            this.tb_smooth.Location = new System.Drawing.Point(114, 227);
            this.tb_smooth.Name = "tb_smooth";
            this.tb_smooth.Size = new System.Drawing.Size(59, 22);
            this.tb_smooth.TabIndex = 21;
            this.tb_smooth.Text = "0";
            this.tb_smooth.Validating += new System.ComponentModel.CancelEventHandler(this.tb_smooth_Validating);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(22, 232);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(41, 12);
            this.label4.TabIndex = 22;
            this.label4.Text = "Smooth";
            // 
            // bt_tip
            // 
            this.bt_tip.Location = new System.Drawing.Point(125, 448);
            this.bt_tip.Name = "bt_tip";
            this.bt_tip.Size = new System.Drawing.Size(48, 25);
            this.bt_tip.TabIndex = 23;
            this.bt_tip.Text = "Tip";
            this.bt_tip.UseVisualStyleBackColor = true;
            this.bt_tip.Click += new System.EventHandler(this.bt_tip_Click);
            // 
            // setting_dialog
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.ClientSize = new System.Drawing.Size(202, 485);
            this.Controls.Add(this.bt_tip);
            this.Controls.Add(this.tb_smooth);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.chk_PSA);
            this.Controls.Add(this.chk_islog);
            this.Controls.Add(this.tb_wavnum);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.bt_cancel);
            this.Controls.Add(this.bt_applybt_apply);
            this.Controls.Add(this.bt_OK);
            this.Controls.Add(this.tb_sourcpath);
            this.Controls.Add(this.tb_objnum);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.bt_load);
            this.Controls.Add(this.tb_targetz);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.tb_ypix);
            this.Controls.Add(this.tb_xpix);
            this.Controls.Add(this.tb_ywid);
            this.Controls.Add(this.tb_xwid);
            this.Controls.Add(this.lab_ypix);
            this.Controls.Add(this.lab_xpix);
            this.Controls.Add(this.lab_ywidth);
            this.Controls.Add(this.lab_xwidth);
            this.Name = "setting_dialog";
            this.Text = "setting_dialog";
            this.Load += new System.EventHandler(this.setting_dialog_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lab_xwidth;
        private System.Windows.Forms.Label lab_ywidth;
        private System.Windows.Forms.Label lab_ypix;
        private System.Windows.Forms.Label lab_xpix;
        private System.Windows.Forms.TextBox tb_xwid;
        private System.Windows.Forms.TextBox tb_ywid;
        private System.Windows.Forms.TextBox tb_xpix;
        private System.Windows.Forms.TextBox tb_ypix;
        private System.Windows.Forms.TextBox tb_targetz;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button bt_load;
        private System.Windows.Forms.TextBox tb_objnum;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox tb_sourcpath;
        private System.Windows.Forms.Button bt_OK;
        private System.Windows.Forms.Button bt_applybt_apply;
        private System.Windows.Forms.Button bt_cancel;
        private System.Windows.Forms.TextBox tb_wavnum;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.CheckBox chk_islog;
        private System.Windows.Forms.CheckBox chk_PSA;
        private System.Windows.Forms.TextBox tb_smooth;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button bt_tip;
    }
}