
import React, { useEffect, useState } from 'react';
import { getMargins, updateMargin } from '../services/api';
import { Save, LogOut, DollarSign, Loader } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
  const [margins, setMargins] = useState([]);
  const [products, setProducts] = useState([
    { name: 'HAS ALTIN', key: 'HAS ALTIN' },
    { name: 'ONS', key: 'ONS' },
    { name: 'GRAM ALTIN', key: 'GRAM ALTIN' },
    { name: '22 AYAR', key: '22 AYAR' },
    { name: '14 AYAR', key: '14 AYAR' },
    { name: 'ÇEYREK ALTIN', key: 'ÇEYREK ALTIN' },
    { name: 'YARIM ALTIN', key: 'YARIM ALTIN' },
    { name: 'TAM ALTIN', key: 'TAM ALTIN' },
    { name: 'ATA ALTIN', key: 'ATA ALTIN' },
    { name: 'USD', key: 'USD' },
    { name: 'EUR', key: 'EUR' },
  ]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(null); // stores key of item being saved
  const navigate = useNavigate();

  useEffect(() => {
    fetchMargins();
  }, []);

  const fetchMargins = async () => {
    try {
      const data = await getMargins();
      setMargins(data);
    } catch (error) {
      console.error('Error fetching margins:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMarginValue = (key, field) => {
    const m = margins.find((i) => i.product_name_key === key);
    return m ? m[field] : 0;
  };
  
  const getIsPercentage = (key) => {
    const m = margins.find((i) => i.product_name_key === key);
    return m ? m.is_percentage : false;
  };


  const handleCreateOrUpdate = async (key, amount, amountBuy, amountSell, isPercent) => {
    setSaving(key);
    try {
      let numAmount = parseFloat(amount); if (isNaN(numAmount)) numAmount = 0;
      let numBuy = parseFloat(amountBuy); if (isNaN(numBuy)) numBuy = 0;
      let numSell = parseFloat(amountSell); if (isNaN(numSell)) numSell = 0;

      await updateMargin({
        product_name_key: key,
        margin_amount: numAmount,
        margin_buy: numBuy,
        margin_sell: numSell,
        is_percentage: isPercent
      });
      await fetchMargins(); // Refresh to ensure sync
    } catch (error) {
      console.error(error);
      alert('Kaydetme hatası! Sadece sayı giriniz.');
    } finally {
      setSaving(null);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/adminyonetim_log_tr');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center text-white">
        <Loader className="animate-spin mr-2" /> Yükleniyor...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-white">Admin Paneli - Kar Marjı Yönetimi</h1>
          <button 
            onClick={handleLogout}
            className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition"
          >
            <LogOut size={18} /> Çıkış
          </button>
        </div>

        <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map((product) => (
                <div key={product.key} className="bg-gray-700/50 p-4 rounded-lg border border-gray-600">
                  <h3 className="text-lg font-semibold text-yellow-500 mb-4">{product.name}</h3>

                  <div className="space-y-4">
                    {/* Standard Margin */}
                    <div>
                      <label className="block text-xs text-yellow-500 mb-1 font-bold">Genel Makas (±)</label>
                      <input
                        type="number"
                        step="0.01"
                        defaultValue={getMarginValue(product.key, 'margin_amount')}
                        id={`input-margin-${product.key}`}
                        className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm focus:border-yellow-500 focus:outline-none"
                        placeholder="Alıştan düş, Satışa ekle"
                      />
                    </div>

                    {/* Extra Buy/Sell */}
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <label className="block text-xs text-green-400 mb-1">Ekstra Alış (+/-)</label>
                        <input
                          type="number"
                          step="0.01"
                          defaultValue={getMarginValue(product.key, 'margin_buy')}
                          id={`input-buy-${product.key}`}
                          className="w-full bg-gray-800 border border-green-700/50 rounded px-2 py-1 text-white text-sm focus:border-green-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-red-400 mb-1">Ekstra Satış (+/-)</label>
                        <input
                          type="number"
                          step="0.01"
                          defaultValue={getMarginValue(product.key, 'margin_sell')}
                          id={`input-sell-${product.key}`}
                          className="w-full bg-gray-800 border border-red-700/50 rounded px-2 py-1 text-white text-sm focus:border-red-500 focus:outline-none"
                        />
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        id={`check-${product.key}`}
                        defaultChecked={getIsPercentage(product.key)}
                        className="w-4 h-4 rounded border-gray-600 text-yellow-500 focus:ring-yellow-500 bg-gray-800"
                      />
                      <label htmlFor={`check-${product.key}`} className="text-xs text-gray-300">Tüm değerleri % olarak uygula</label>
                    </div>

                    <button
                      onClick={() => {
                        const valMargin = document.getElementById(`input-margin-${product.key}`).value;
                        const valBuy = document.getElementById(`input-buy-${product.key}`).value;
                        const valSell = document.getElementById(`input-sell-${product.key}`).value;
                        const isPerc = document.getElementById(`check-${product.key}`).checked;
                        handleCreateOrUpdate(product.key, valMargin, valBuy, valSell, isPerc);
                      }}
                      disabled={saving === product.key}
                      className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded transition disabled:opacity-50 text-sm"
                    >
                      {saving === product.key ? <Loader className="animate-spin" size={16} /> : <Save size={16} />}
                      Tümünü Kaydet
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
