import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import SocialAuthentication from "@/features/auth/SocialAuthentication";
import SignInForm from "./SignInForm";

const SignInCard = () => {
    return (
        <Card className="w-[300px] md:w-[350px] lg:w-[370px]">
            <CardHeader>
                <CardTitle>Ready to Continue?</CardTitle>
                <CardDescription>
                    Log in now to continue reading your favorite articles,
                    comment on discussions, and enjoy new content&rsquo;
                </CardDescription>
            </CardHeader>
            <CardContent>
                <SignInForm />
            </CardContent>
            <CardFooter>
                <SocialAuthentication />
            </CardFooter>
        </Card>
    );
};

export default SignInCard;
