#########################################
# IMPORT SoftwareAI Libs 
from CoreApp._init_libs_ import *
#########################################



def keys_app_2():
        
    cred1 = {
    "type": "service_account",
    "project_id": "aicompanydata2",
    "private_key_id": "f548ed98ab5bd94af46c380cc76b3ecfe0dead68",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQDdTXlRyv56igXy\nVHYi4sYYTSm22mRpz3xPLvqQvGtjWoZ3+HCQn33lOnst04gFYPAeoCDF4hiG3aL4\nAd2IfdfC8TdQxOqc49FxWlSXXRIY2lZf2h0rpouUrJMfayu+lZCP2y3oATvv37PK\n1HsFB/B98yr6aLnMyGUSDxKOPAKerNUmTCZKqSXllTw8ks6xLtW48xUOkZriHnhk\njTm8EaG3DwIDUWABWda5nvPvpZH9KMUhWU5rjVhVS/sHd2JmIoZMcykHjnmNbwX7\nCA8q9JBqOjIBu8fU678oR1SPBEMDKYKd11Ph9FkINn7M1ZFLQCqpDjwQBU/6z+FO\nz5YgXH9xAgMBAAECgf8LIl4Y2FZRbl8hVm4eid3/XO0N27G0Cp6uWlaH7tBr5XC0\nWUCQ1zgS8nXKK+Ai/KHIkHfEJ6pf/SiFfAlu2098X8JUk/tJNTmWljf/tDVK7/g7\ne288hpW9jumPLnkmhSdThb4WPcAgX93UJ6u6OBGsxQ7KI+zXPkaARwOJTbFUh7Li\ncs3ar33MVcKNwv+b7vYCfm8gW/05SXL0ueu4MjeGGJC5DuLOxQ4Fg+z6wpPYVkXS\nxMYTrGAOdJXflSC4Y7Ygrlh9xbfsYHXdcXdBSpRcINoJTP1AT4KamvVskRQh0zNy\n7DqrLKhFOABIsPrKPrPJpqYYSOUWE3lTQKRDhBUCgYEA/YVFvSb3DLyoLTIkLf/N\nljWL3oNGCHqR90rMrLt5XmOlakPR7s0nfRT9Dm3xKh7vOaOqbSWhkCK9UMJKoFI6\nGuYdaDQUqr1FzjK/BWAg5Zf9WMBzr4IlXoak3sW2JhFZWPzQvUPzk7+ArZMc9EKo\nI2cVUNdRBvvNaxjeOSL5Qn8CgYEA33eJ9KdmhSlmGLIf1jbwYXiAaTEo5MIqC95d\nBHo2q5lr10Xm8lglTWobKoDNz0wo6Sa7pydyin8/SGW3arI7ssgqQH11o5UF+SLb\n4jteSZykD4ZPU/8sj/ZcLBoNQjH11YBX8qHRIGqDT3WnicoRG/k4YCgow9GVSlre\nS5U9Zg8CgYA6ovaMV1TQt1nWikBf+0hbs6rUHly2XVMhdUV9tibONBHwUBtgNkcp\n4Q7epYMgEOOX20jx0cBajA5pfWaxShNyYULv9QvKqdhZZtdTsPYq5EqOmoSnVVy7\nTj0X4XbNuzmFIYROIkdWJvbmLp6FyF0HQzJk7kgpa1gJq0jKwlIQlQKBgCDr5HgV\nnWXqxm7G9yfA6kMB1LEqm+KvtDARb1S0iI9ZR+jsFG0JjV1NT3lAhpGOn8xRd33V\nsusyeek5iv7+CQt6r7bWhNk3oCym9QvsQSTJHeZnnBI82pzO559bqy5gW947TTmi\nm0OSTYwMQkVrbn/XhHWuFOtcWgkdP/iUoPoDAoGAZV1vSQkXWTUVjG/MOKra6M8b\n49HFPw7C4wvYNkD1uGC6FW1nSaYVyQzB2oPnuZzjUat/aHoHiTzZlnmT027wGB57\nh8HvXECY4SXtMkDTp/lNPqpRd1j8/IBtDvwGrL4XOgHlGROpy2IDqEd1Rur2wS+J\nS6c0QzDVFgLPE5Vc/tI=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-z7lro@aicompanydata2.iam.gserviceaccount.com",
    "client_id": "111147579049081138001",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-z7lro%40aicompanydata2.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }
    credt1 = credentials.Certificate(cred1)
    app2 = initialize_app(credt1, {
            'storageBucket': 'aicompanydata2.appspot.com',
            'databaseURL': 'https://aicompanydata2-default-rtdb.firebaseio.com'
    }, name='app2')

    return app2



def keys_app_1():
        

    cred1 = {
    "type": "service_account",
    "project_id": "aicompanydata1",
    "private_key_id": "4df4717af337b5cc786856f7468db6777e0d95f3",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDKWTw1NgTL1ANx\niwp6JdOUEMRTsGWbnz6qSX+kgGDPWWcX5w5xTGlHO1Loz/82TyghL31rTBgYLYYm\najmIUz+FlKZhiByFYA4CV4tNdOqv1/e2XnGlexF5o5sik9gB7bn5wIppjeuOtJNA\ne07eTWfnVboGxTrcrb6cgfImi3xluJSKNJ5Cc84jz7fhRmLXASvveR9IAQYX2pFc\nS2j2swnFjr54Un2QYQNxxdYrWQQJasDkP9iAHQ/LGE1xj/1JY6DepPGobosvUTx4\nnOli4wyEPeTPlCzA4XH3MROJCEVDIKsPaETi7j9ZsIeJLWpgY/AXOYtbVkFCxHEE\nkz/HgIILAgMBAAECggEADK5apBkOZDnAEim9DoT4BVj8UiRavHiBObR2eo2Nw6De\nNvTE28aGoy9YFagSCJ9zATVpM5lmudPXNZQa++yqV/RGGGmqeT9Y/BOWyClncH1l\nPvlx6jApcF6XoStJHRcpZw9b0pv8IwrftD77ZS95BK9Dg8YbghX6Ep6K2ZiMmLvu\nhDz1TNZ+ggyxP47E6TnEAQdvbbm5tMStd6GkqxYckGpiiMIjUR+OM/AxSAr0MhDA\nvfgPqMTfRDLkeRICrxSImQt/j0lV+b9m5g/3W+NVkarQLSVADkVZzpgDJx2glmj4\nrgzWYvvM+x4vXCmrqLIIiexPQc6EKEH75ce6fpF46QKBgQDycz9ai0U/RSt3JYU3\nLjR3LsjpL9BKwpOA/KXjlUmik8H02SmbxHc4PHCelz+nB0EkAEuNjk4AUlycS9Q1\nITSPIMKE7kksReNYBT+6Q/OvpQP8QBYNDGXOt422nAz1sQ0YawNmnp0HePE4mgfg\nkWpOEAgyAmAogmSfvJdJD6tTqQKBgQDVqEBEF4PzEqy7Yidsy2xho1BZrMk5/6Sw\nmDbwbbGvrB2SC6e9Y88olESiTdlLPkB//zxmkT9IlRK0VsR+Ans8Ztr1mLuxzj1+\njbeemMyN2lncww36wJoCI6HMvOW4uBgYtnqiwLdmdt6MJtuAVRD4qMMDeF54e9gN\njFzkAs64kwKBgQCq/PSVWtt/f7zjzqZhAEkoNOqk6n+v+gIlWgl0s/i2nBaSJAXg\nQXMDSjzy3CCcH9WlGkAumUoRmASQhjonLj/vIV+OeK9Kdg+cKDeFmh7mpS5mXJww\nn6m9XF6phuzs6e0eZ3qCiSKd/oHBNYCQtH2QiGX/PwWqDCwDK/JWKKLf4QKBgQC8\nvYL4I+XWRrr8VXsKarF1lzWV4kNozuKHdg+iWOTMkTkWGOG3NoJ8EG6JCkhYZcfI\nyopq+Qh0b+w0DypJPpvrAdmPd7rnGY/NShfZLJYXAbq8gDrLNnVWSm/WU1CD22y9\n+AVh3OimxX9XQ8RIG92ALGUJnb2mpZB4d3Rfn/NJrQKBgF/9n/2rBIbK2OO0cPNG\nszm/bHRzfzoM87p9IbfgaYsp2DrD7ikTaWLLwiT/alphXvnDBOiTf0lO8VNzR/Dy\n3lb3yWqrLywSfgV+lWpKXRsJvsLP4tqKidaSPspcGUXIVm3gv4h83JFAgx51j0c6\nGrMTImOhpohyjYJOfZ7Q5Nyg\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-47yps@aicompanydata1.iam.gserviceaccount.com",
    "client_id": "102000584574845908426",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-47yps%40aicompanydata1.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }
    credt1 = credentials.Certificate(cred1)
    app1 = initialize_app(credt1, {
            'storageBucket': 'aicompanydata1.appspot.com',
            'databaseURL': 'https://aicompanydata1-default-rtdb.europe-west1.firebasedatabase.app'
    }, name='app1')

    return app1


def keys_app_x():
        

        cred1 = {
        "type": "service_account",
        "project_id": "aicompanydata1",
        "private_key_id": "4df4717af337b5cc786856f7468db6777e0d95f3",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDKWTw1NgTL1ANx\niwp6JdOUEMRTsGWbnz6qSX+kgGDPWWcX5w5xTGlHO1Loz/82TyghL31rTBgYLYYm\najmIUz+FlKZhiByFYA4CV4tNdOqv1/e2XnGlexF5o5sik9gB7bn5wIppjeuOtJNA\ne07eTWfnVboGxTrcrb6cgfImi3xluJSKNJ5Cc84jz7fhRmLXASvveR9IAQYX2pFc\nS2j2swnFjr54Un2QYQNxxdYrWQQJasDkP9iAHQ/LGE1xj/1JY6DepPGobosvUTx4\nnOli4wyEPeTPlCzA4XH3MROJCEVDIKsPaETi7j9ZsIeJLWpgY/AXOYtbVkFCxHEE\nkz/HgIILAgMBAAECggEADK5apBkOZDnAEim9DoT4BVj8UiRavHiBObR2eo2Nw6De\nNvTE28aGoy9YFagSCJ9zATVpM5lmudPXNZQa++yqV/RGGGmqeT9Y/BOWyClncH1l\nPvlx6jApcF6XoStJHRcpZw9b0pv8IwrftD77ZS95BK9Dg8YbghX6Ep6K2ZiMmLvu\nhDz1TNZ+ggyxP47E6TnEAQdvbbm5tMStd6GkqxYckGpiiMIjUR+OM/AxSAr0MhDA\nvfgPqMTfRDLkeRICrxSImQt/j0lV+b9m5g/3W+NVkarQLSVADkVZzpgDJx2glmj4\nrgzWYvvM+x4vXCmrqLIIiexPQc6EKEH75ce6fpF46QKBgQDycz9ai0U/RSt3JYU3\nLjR3LsjpL9BKwpOA/KXjlUmik8H02SmbxHc4PHCelz+nB0EkAEuNjk4AUlycS9Q1\nITSPIMKE7kksReNYBT+6Q/OvpQP8QBYNDGXOt422nAz1sQ0YawNmnp0HePE4mgfg\nkWpOEAgyAmAogmSfvJdJD6tTqQKBgQDVqEBEF4PzEqy7Yidsy2xho1BZrMk5/6Sw\nmDbwbbGvrB2SC6e9Y88olESiTdlLPkB//zxmkT9IlRK0VsR+Ans8Ztr1mLuxzj1+\njbeemMyN2lncww36wJoCI6HMvOW4uBgYtnqiwLdmdt6MJtuAVRD4qMMDeF54e9gN\njFzkAs64kwKBgQCq/PSVWtt/f7zjzqZhAEkoNOqk6n+v+gIlWgl0s/i2nBaSJAXg\nQXMDSjzy3CCcH9WlGkAumUoRmASQhjonLj/vIV+OeK9Kdg+cKDeFmh7mpS5mXJww\nn6m9XF6phuzs6e0eZ3qCiSKd/oHBNYCQtH2QiGX/PwWqDCwDK/JWKKLf4QKBgQC8\nvYL4I+XWRrr8VXsKarF1lzWV4kNozuKHdg+iWOTMkTkWGOG3NoJ8EG6JCkhYZcfI\nyopq+Qh0b+w0DypJPpvrAdmPd7rnGY/NShfZLJYXAbq8gDrLNnVWSm/WU1CD22y9\n+AVh3OimxX9XQ8RIG92ALGUJnb2mpZB4d3Rfn/NJrQKBgF/9n/2rBIbK2OO0cPNG\nszm/bHRzfzoM87p9IbfgaYsp2DrD7ikTaWLLwiT/alphXvnDBOiTf0lO8VNzR/Dy\n3lb3yWqrLywSfgV+lWpKXRsJvsLP4tqKidaSPspcGUXIVm3gv4h83JFAgx51j0c6\nGrMTImOhpohyjYJOfZ7Q5Nyg\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-47yps@aicompanydata1.iam.gserviceaccount.com",
        "client_id": "102000584574845908426",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-47yps%40aicompanydata1.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
        }
        credt1 = credentials.Certificate(cred1)
        appx = initialize_app(credt1, {
                'storageBucket': 'aicompanydata1.appspot.com',
                'databaseURL': 'https://aicompanydata1-default-rtdb.europe-west1.firebasedatabase.app'
        }, name='appx')

        return appx




                    
def keys_teste():
    cred1 = {
  "type": "service_account",
  "project_id": "teste-v-d5b18",
  "private_key_id": "b8dfc6c41c28af0d6479c88421263e1c2b6c535c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCvGiHhrvY4aigm\nFBF7EzZMRPLqtGWGEawIXttzzCd6JEosOv9LLf6VUKlk+HgbF/w5zglWA+KYfaS4\n5ud4XihkdhKQRl3eD7VUku9sL/5OubdR5hfj6lPFOvDkHEN7hdEub5HxMrBCkwZX\nl0xZWN9FqgRF3CE+14miYN4Zh2VVqjayA4bSNUBiDtwv0njQPQjXa/C9cHzS1eQG\nkX5vyCe6Hfkq+Z28ibBl/95ikZfoA9MykM7aGWPeWjMJIlSGxkWPRkRCCFiyKtOi\nI/jHuqGbhpyKSR59htKlSxb8Q37iMr2novW0dEedRBCvyoYjnaFA0AIOUTsCTf0o\nQ3QwQIzZAgMBAAECggEAD2SmDdz/sD3vgZ7KBUkka4K0Mts2Vu7pcg2aD+Kmpcot\nlcMp+5tI13+GehCNyR6hVxjnITSo5ZbwtYCMYLyGTdlDZdjfGk0Z4nF4XXO/+35q\nwJG7D+zi/be3bZY+fcwUc5dDUTI6OeAK8rBOT0ciJFGp8SpE50KzdXQ753/2R0LQ\nfJQ3weqkHEJEjx8Nm2vQRyeLRLNtMSGlIE2T8Y0CZurhwGTRlEMQOhfXPTqrwcaQ\nLx3fUV81ndTnxRtRYmd8mpealMw2RAUDZujpafwoHO6Q3ePwPT3MYcMHuVtkxsmi\nHR/4mver8fMr00IxRz3FcbMKH86vueTf6QTS9O4EMQKBgQC3TLSZprhHtcuEo3u1\n2iLLDHm5LPPNq/LUOhDO+ezKfa4cGClLVGIZ+g5qNyjrOGFDCEIydX1fXloPfGl4\nsW6CBEpcBAtdEHfOMnmVN/2gGlJwmaQ784q/wPfUPV2VGoFKLUvq4b5rLFJioGko\nZ+P3HmZsTL9tkp7Jzm9v7ps56wKBgQD0jRcK/nk1RU6fHUVPnmpLpJAeBMjoiToc\nkY08B47/sMwjbh2MtzgJP1QJ1eRV3xsoxDHjG0UH49XxsawwH1xt1zlK7WidTWzI\nHtc5MND/NHrzC0TQAIDy3A6WnsRYPD2WA5QbVyvO3HRqSzAb915WNP56FJiEmQLV\nmXwJv2F/SwKBgHMoAIpLgJiksNCKuMzd12ADXXGluSGsdik4tZii0U3BuaGy2DaY\nM+2n+GhocQ+d4xTu2k/DGlnQ9/mkqsqFhiyur1yxucXk86+abGH/xBpSjxponBKC\nBdhETi6LwwBKn5FPddOBsVS5iqSlrIsTAdgdxDEj4lvfclzMkZwbpm+zAoGBAIX0\nCp0xCr+NOSWa6O5Vva+1cmOfB1WoZTZk29H36fJQq2D03ibH7V/TWnsQuEP5M20/\nGnxl4YgS2ovLYJ/zbbOU4oMSS+1uDZoImqdu/+vqmTYsBANTY06kDzGdwbr7NFjJ\nmQTo2Mw0oWffy3hmJTxfRs0kHu7yyUSrD/Be7k7FAoGAcDEiyW2IXjKIsnB3WYpk\n90U/TYLIh2rxIQpLYndKmyOMhQtUOgCg9iaxONCQAVkT8jnzn6KJI5vLelWze1eH\nl2pINs1D+q6TxwXG1s0dr/jN2x0WvnU92w0c5NfrOpMFo18Rup645TZEE9tMJNZn\n7z/BxNS5voWcQNmzsXAPeJ0=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-uyz41@teste-v-d5b18.iam.gserviceaccount.com",
  "client_id": "111238680143279523841",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-uyz41%40teste-v-d5b18.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

    credt1 = credentials.Certificate(cred1)
    teste = initialize_app(credt1, {
            'storageBucket': 'aicompanydata1.appspot.com',
            'databaseURL': 'https://aicompanydata1-default-rtdb.europe-west1.firebasedatabase.app'
    }, name='teste')
    return teste
    
            