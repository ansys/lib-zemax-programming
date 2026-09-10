using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZOSAPI;

namespace Diffractive_DLL_Setup_Assistant
{
    public partial class Form1 : Form
    {
        IOpticalSystem TheSystem;
        public Form1(IOpticalSystem receive_TheSystem)
        {
            TheSystem = receive_TheSystem;
            InitializeComponent();
            KeyPreview = true;
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            auto_detect_single_object();
            loadpar();
            loadvalue();
            auto_detect_objects();
        }
        bool is_load_diff_DLL(int objnum, bool showerror = true)
        {
            if (!(objnum > 0 && objnum <= TheSystem.NCE.NumberOfObjects))
            {
                if (showerror) MessageBox.Show("Invalid object number");
            }
            else if (!TheSystem.NCE.GetObjectAt(objnum).DiffractionData.IsDiffractionAvailable)
            {
                if (showerror) MessageBox.Show("Object #" + objnum.ToString() + " does not has a diffraction face.");
            }
            else if (TheSystem.NCE.GetObjectAt(objnum).DiffractionData.Split != ZOSAPI.Editors.NCE.DiffractionSplitType.SplitByDLL)
            {
                if (showerror) MessageBox.Show("Object #" + objnum.ToString() + " does not load a diffraction DLL.");
            }
            else if (TheSystem.NCE.GetObjectAt(objnum).DiffractionData.NumberOfParameters == 0)
            {
                if (showerror) MessageBox.Show("This DLL \"" + TheSystem.NCE.GetObjectAt(objnum).DiffractionData.DLL + "\" doesn't has any parameter.");
            }
            else
            {
                Console.WriteLine("Object# " + objnum.ToString() + " is loading a diffraction DLL.");
                return true;
            }
            Console.WriteLine("Object# " + objnum.ToString() + " doesn't load a diffraction DLL.");
            return false;
        }
        int parse_single_object_number(bool showerror = true)
        {
            if (!int.TryParse(tb_single_obj.Text, out int objnum)
                || !is_load_diff_DLL(objnum))
            {
                if (showerror)
                    MessageBox.Show("Invalid Object#: " + tb_single_obj.Text);
                Console.WriteLine("Cannot parse object number for Object# " + tb_single_obj.Text);
                return 0; 
            }
            return objnum;
        }
        List<int> ParseStringToIntList(string str)
        {
            List<int> result = new List<int>();
            string[] parts = str.Split(',');
            foreach (string part in parts)
            {
                if (part.Contains("-"))
                {
                    string[] dashParts = part.Split('-');
                    if (dashParts.Length != 2 ||
                        !int.TryParse(dashParts[0], out int start) ||
                        !int.TryParse(dashParts[1], out int end))
                    {
                        MessageBox.Show("Invalid format: " + part);
                        return new List<int>();
                    }
                    else if (start > end)
                    {
                        MessageBox.Show("Invalid range: " + part);
                        return new List<int>();
                    }
                    else
                        for (int i = start; i <= end; i++)
                            result.Add(i);
                }
                else
                {
                    if (!int.TryParse(part, out int num))
                    {
                        MessageBox.Show("Invalid format: " + part);
                        return new List<int>();
                    }
                    result.Add(num);
                }
            }
            string tmpstr = "";
            foreach (int i in result)
                tmpstr += i.ToString() + ", ";
            Console.WriteLine("Parse String \"" + str +
                "\" To Int List [" + tmpstr.Remove(tmpstr.Length - 2) + "]");
            return result;
        }
        List<double> ParseStringToDoubleList(string str)
        {
            List<double> result = new List<double>();
            string[] parts = str.Split(',');
            foreach (string part in parts)
            {
                if (!double.TryParse(part, out double num))
                {
                    MessageBox.Show("Invalid format: " + part);
                    return new List<double>();
                }
                result.Add(num);
            }
            string tmpstr = "";
            foreach (double d in result)
                tmpstr += d.ToString() + ", ";
            Console.WriteLine("Parse String \"" + str +
                "\" To Double List [" + tmpstr.Remove(tmpstr.Length - 2) + "]");
            return result;
        }
        List<int> get_multiple_object_numbers()
        {
            string str = tb_objects.Text;
            List<int> result = ParseStringToIntList(str);
            if (result.Count == 0)
                return result;

            string msg_obj_removed = "";
            for (int i = 0; i < result.Count; i++)
                if (!is_load_diff_DLL(result[i]))
                {
                    msg_obj_removed += result[i].ToString() + ", ";
                    result.RemoveAt(i);
                    i--;
                }
            if (msg_obj_removed != "")
                MessageBox.Show(
                    "These objects are removed as they don't load a diffractive DLL:\n "
                    + msg_obj_removed.Remove(msg_obj_removed.Length - 2));

            if (result.Count == 0)
                MessageBox.Show("No any valid objects are defined");

            string msg = "";
            foreach (int obj in result)
                msg += obj.ToString() + ", ";
            Console.WriteLine("Parsed multiple object#: " + msg.Remove(msg.Length - 2));

            return result;
        }

        List<int> parse_parnums(int objnum)
        {
            string str = tb_parameters.Text;
            List<int> parnums = ParseStringToIntList(str);
            if (parnums.Count == 0)
                return new List<int>();
            for (int i = 0; i < parnums.Count; i++)
                if (parnums[i] > TheSystem.NCE.GetObjectAt(objnum).DiffractionData.NumberOfParameters)
                {
                    parnums.RemoveAt(i);
                    i--;
                }
            if (parnums.Count == 0)
                MessageBox.Show("Non of specified parameter numbers are availalbe for object " + objnum.ToString());

            string msg = "";
            foreach (int par in parnums)
                msg += par.ToString() + ", ";
            Console.WriteLine("Parsed par#: " + msg.Remove(msg.Length - 2));

            return parnums;
        }
        List<double> parse_values()
        {
            string str = tb_values.Text;
            List<double> values = ParseStringToDoubleList(str);
            if (values.Count == 0)
                return new List<double>();

            string msg = "";
            foreach (int val in values)
                msg += val.ToString() + ", ";
            Console.WriteLine("Parsed values: " + msg.Remove(msg.Length - 2));

            return values;
        }
        void loadpar()
        {
            int objnum = parse_single_object_number();
            if (objnum == 0) return;
            int num_of_par = TheSystem.NCE.GetObjectAt(objnum).DiffractionData.NumberOfParameters;
            tb_parameters.Text = "1 - " + num_of_par.ToString();
        }
        private void b_loadpar_Click(object sender, EventArgs e)
        {
            loadpar();
        }
        void loadvalue()
        {
            int objnum = parse_single_object_number();
            if (objnum == 0) return;
            string valuestr = "";
            List<int> parnums = parse_parnums(objnum);
            if (parnums.Count == 0) return;
            // num_of_par should not be zero as it's already checked by is_load_diff_DLL()
            for (int i = 0; i < parnums.Count; i++)
                valuestr += TheSystem.NCE.GetObjectAt(objnum).DiffractionData.GetReflectParameterValue(parnums[i] - 1).ToString() + ",  ";
            tb_values.Text = valuestr.Remove(valuestr.Length - 3);
        }
        private void b_loadvalue_Click(object sender, EventArgs e)
        {
            loadvalue();
        }

        private void b_setMCE_Click(object sender, EventArgs e)
        {
            List<int> objs = get_multiple_object_numbers();
            if (objs.Count == 0) return;

            foreach (int obj in objs)
                if (TheSystem.NCE.GetObjectAt(obj).DiffractionData.DLL != TheSystem.NCE.GetObjectAt(obj).DiffractionData.DLL)
                {
                    MessageBox.Show("Specified object " + obj.ToString() + " load a DLL that is different to input object " + obj.ToString());
                    return;
                }
            
            List<int> parnums = parse_parnums(objs[0]);
            if (parnums.Count == 0) return;

            var TheMCE = TheSystem.MCE;

            TheSystem.TheApplication.ShowChangesInUI = false;
            foreach (int obj in objs)
                foreach (int par in parnums)
                {
                    int num_mceop = TheMCE.NumberOfOperands;
                    TheMCE.InsertNewOperandAt(num_mceop + 1);
                    TheMCE.InsertNewOperandAt(num_mceop + 1);
                    string par_name = TheSystem.NCE.GetObjectAt(obj).DiffractionData.GetReflectParameterName(par - 1);
                    var op1 = TheMCE.GetOperandAt(num_mceop + 1);
                    var op2 = TheMCE.GetOperandAt(num_mceop + 2);
                    op1.GetOperandCell(1).Value = par_name;
                    op2.ChangeType(ZOSAPI.Editors.MCE.MultiConfigOperandType.NPRO);
                    op2.Param2 = obj;
                    op2.Param3 = par + 300;
                }

            if (chk_set_trans.Checked)
            {
                int counter = 0;
                int mce_operand_num;
                foreach (int obj in objs)
                    foreach (int par in parnums)
                    {
                        mce_operand_num = TheMCE.NumberOfOperands;
                        TheMCE.InsertNewOperandAt(mce_operand_num + 1);
                        var op = TheMCE.GetOperandAt(mce_operand_num + 1);
                        op.ChangeType(ZOSAPI.Editors.MCE.MultiConfigOperandType.NPRO);
                        op.Param2 = obj;
                        op.Param3 = par + 350;
                        var solvetype = TheMCE.GetOperandAt(mce_operand_num + 1).GetOperandCell(1).CreateSolveType(ZOSAPI.Editors.SolveType.ConfigPickup);
                        solvetype._S_ConfigPickup.Configuration = 1;
                        solvetype._S_ConfigPickup.Operand = mce_operand_num - counter - (parnums.Count * objs.Count - 1) * 2 + counter * 2;
                        TheMCE.GetOperandAt(mce_operand_num + 1).GetOperandCell(1).SetSolveData(solvetype);
                        counter++;
                    }
            }
            MessageBox.Show("Set MCE done!");
        }

        private void b_set_parameter_Click(object sender, EventArgs e)
        {
            List<int> objs = get_multiple_object_numbers();
            if (objs.Count == 0) return;

            foreach (int obj in objs)
                if (TheSystem.NCE.GetObjectAt(obj).DiffractionData.DLL != TheSystem.NCE.GetObjectAt(objs[0]).DiffractionData.DLL)
                {
                    MessageBox.Show("Specified object " + obj.ToString() + " load a DLL that is different to the other object " + objs[0].ToString());
                    return;
                }

            List<int> parnums = parse_parnums(objs[0]);
            if (parnums.Count == 0) return;

            List<double> values = parse_values();
            if (values.Count != parnums.Count)
            {
                MessageBox.Show("Number of Par# is not same as number of Values. Please check the input.");
                return; 
            }

            foreach (int obj in objs)
            {
                for (int i = 0; i < parnums.Count; i++)
                {
                    TheSystem.NCE.GetObjectAt(obj).DiffractionData.SetReflectParameterValue(parnums[i] - 1, values[i]);
                    if (chk_set_trans.Checked)
                        TheSystem.NCE.GetObjectAt(obj).DiffractionData.SetTransmitParameterValue(parnums[i] - 1, values[i]);
                }
            }
            MessageBox.Show("Set parameters done!");
        }
        private void b_copy_par_Click(object sender, EventArgs e)
        {
            int objnum = parse_single_object_number();
            if (objnum == 0) return;

            List<int> parnums = parse_parnums(objnum);
            if (parnums.Count == 0) return;

            List<int> objs = get_multiple_object_numbers();
            if (objs.Count == 0) return;

            foreach (int obj in objs)
                if (TheSystem.NCE.GetObjectAt(obj).DiffractionData.DLL != TheSystem.NCE.GetObjectAt(objnum).DiffractionData.DLL)
                {
                    MessageBox.Show("Specified object " + obj.ToString() + " load a DLL that is different to input object " + objnum.ToString());
                    return;
                }


            foreach (int obj in objs)
                foreach (int par in parnums)
                {
                    TheSystem.NCE.GetObjectAt(obj).DiffractionData.SetReflectParameterValue(par - 1,
                        TheSystem.NCE.GetObjectAt(objnum).DiffractionData.GetReflectParameterValue(par - 1));
                    if (chk_set_trans.Checked)
                        TheSystem.NCE.GetObjectAt(obj).DiffractionData.SetTransmitParameterValue(par - 1,
                            TheSystem.NCE.GetObjectAt(objnum).DiffractionData.GetTransmitParameterValue(par - 1));
                }
            MessageBox.Show("Set parameters done!");
        }
        void auto_detect_single_object()
        {
            for (int i = 1; i <= TheSystem.NCE.NumberOfObjects; i++)
                if (is_load_diff_DLL(i, false))
                {
                    tb_single_obj.Text = i.ToString();
                    return;
                }
        }
        void auto_detect_objects()
        {
            string str = "";
            int objnum = parse_single_object_number(false);
            if (objnum == 0)
                for (int i = 1; i <= TheSystem.NCE.NumberOfObjects; i++)
                    if (is_load_diff_DLL(i, false))
                    {
                        objnum = i;
                        break;
                    }
            if (objnum == 0)
            {
                MessageBox.Show("Cannot find any diffractive object.");
                return;
            }
            for (int i = 1; i <= TheSystem.NCE.NumberOfObjects; i++)
                if (TheSystem.NCE.GetObjectAt(i).DiffractionData.DLL == TheSystem.NCE.GetObjectAt(objnum).DiffractionData.DLL)
                    str += i.ToString() + ", ";
            tb_objects.Text = str.Remove(str.Length - 2);
        }

        private void b_detect_obj_Click(object sender, EventArgs e)
        {
            auto_detect_objects();
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
                this.Close();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            DialogResult dialog = MessageBox.Show("Do you want to leave?",
                "Exit", MessageBoxButtons.OKCancel,
                MessageBoxIcon.None,
                MessageBoxDefaultButton.Button1);

            if (dialog != DialogResult.OK)
            {
                e.Cancel = true;
            }
        }

        private void b_LinkOn_Click(object sender, EventArgs e)
        {
            tb_parameters.Text = "5";
            tb_values.Text = "1";
        }

        private void b_LinkOn99_Click(object sender, EventArgs e)
        {
            tb_parameters.Text = "5";
            tb_values.Text = "99";
        }

        private void b_LinkOff_Click(object sender, EventArgs e)
        {
            tb_parameters.Text = "5";
            tb_values.Text = "0";
        }
    }
}
