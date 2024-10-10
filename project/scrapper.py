from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd


class Scrapper(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        super(Scrapper, self).__init__(service=service, options=options)
        self.maximize_window()

    def select_location(self):
        uf_cascade_menu = self.find_element(By.XPATH, '//*[@id="consultarUfAcessoLivre"]')
        go_option = uf_cascade_menu.find_element(By.XPATH, '//*[@id="consultarUfAcessoLivre"]/option[10]')
        go_option.click()

        city_cascade_menu = self.find_element(By.XPATH, '//*[@id="consultarMunicipioAcessoLivre"]')
        morrinhos_option = city_cascade_menu.find_element(By.XPATH,
                                                          '//*[@id="consultarMunicipioAcessoLivre"]/option[152]')
        morrinhos_option.click()

        ano_input = self.find_element(By.XPATH, '//*[@id="consultarAno"]')
        ano_input.send_keys('2024')

        consultar_btn = self.find_element(By.XPATH, '//*[@id="form_submit"]')
        consultar_btn.click()
        self.switch_to.window(self.window_handles[0])

    def access_transfere_gov(self):
        self.get('https://www.gov.br/transferegov/pt-br/sistemas/acesso-livre')

        self.implicitly_wait(5)
        consultar_propostas_btn = self.find_element(By.XPATH, '//*[@id="parent-fieldname-text"]/p[5]/span/a')
        url = consultar_propostas_btn.get_attribute('href')
        self.get(url)

        self.implicitly_wait(1)
        self.select_location()

        self.implicitly_wait(1)
        self.get_data()

    def get_data(self):
        elements = self.find_elements(By.CLASS_NAME, 'odd') + self.find_elements(By.CLASS_NAME, 'even')

        proposal_dict = {"Número da Proposta": [], 'Número do Processo': [], 'Valor Global': []}

        total_value = 0

        for i in range(len(elements)):
            elements = self.find_elements(By.CLASS_NAME, 'odd') + self.find_elements(By.CLASS_NAME, 'even')
            element_and_status = self.get_element_status(elements[i])

            if element_and_status[1] == 'Em execução':
                element_and_status[0].click()
                proposal_number = self.find_element(By.XPATH, '//*[@id="tr-alterarNumeroProposta"]/td[4]').text
                process_number = self.find_element(By.XPATH, '//*[@id="tr-alterarNumeroProcesso"]/td[2]').text
                global_value = self.find_element(By.XPATH,
                                                 '//*[@id="tr-alterarPercentualMinimoContrapartida"]/td/b').text

                global_value = global_value.split(' ')[1].replace('.', '').replace(',', '.')
                total_value += float(global_value)

                proposal_dict['Número da Proposta'].append(proposal_number)
                proposal_dict['Número do Processo'].append(process_number)
                proposal_dict['Valor Global'].append(f'R$ {global_value}')

                self.back()
                self.implicitly_wait(1)

        proposal_dict['Número da Proposta'].append(' ')
        proposal_dict['Número do Processo'].append('Valor Total')
        proposal_dict['Valor Global'].append(f'R$ {str(total_value)}')
        self.generate_table(proposal_dict)

    def get_element_status(self, element):
        status_elements = element.find_elements(By.TAG_NAME, 'a')
        return status_elements[1], status_elements[1].text

    def generate_table(self, proposal_dict):
        df = pd.DataFrame(proposal_dict)

        with pd.ExcelWriter('tabela.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Propostas', index=False)


def main():
    print("Initializing\n")
    scrapper = Scrapper()
    scrapper.access_transfere_gov()


if __name__ == "__main__":
    main()
